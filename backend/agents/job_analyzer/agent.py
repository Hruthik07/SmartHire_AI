import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from backend.agents.resume_analyzer.embeddings import get_embedding, load_id_map
from backend.agents.resume_analyzer.agent import ResumeAnalyzerAgent

load_dotenv()


class JobAnalyzerAgent:
    """
    JobAnalyzerAgent
    ----------------
    - Analyzes job descriptions using LLM.
    - Loads FAISS embeddings and resume IDs from data/embeddings.
    - Matches resumes via FAISS, LLM reasoning, and keyword overlap.
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.prompts_dir = os.path.join("backend", "agents", "job_analyzer", "prompts")

        # FAISS index + JSON ID map
        self.index_path = os.path.join("data", "embeddings", "resume_faiss.index")
        self.id_map_path = os.path.join("data", "embeddings", "resume_ids.json")

        self.resume_agent = ResumeAnalyzerAgent()

    # -------------------------------------------------------
    # Utility: Load FAISS and ID map
    # -------------------------------------------------------
    def _load_index(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(
                f"❌ FAISS index not found at {self.index_path}. "
                "Please rebuild embeddings using /rebuild_embeddings."
            )
        print(f"[DEBUG] ✅ Loading FAISS index from {self.index_path}")
        return faiss.read_index(self.index_path)

    def _load_id_map(self):
        id_map = load_id_map()
        if not id_map:
            raise FileNotFoundError(
                f"❌ No resume ID map found at {self.id_map_path}."
            )
        print(f"[DEBUG] ✅ Loaded {len(id_map)} resumes from ID map.")
        return id_map

    # -------------------------------------------------------
    # Utility: Embedding + Keyword overlap
    # -------------------------------------------------------
    def embed_text(self, text: str) -> np.ndarray:
        vec = get_embedding(text)
        return np.array([vec], dtype="float32")

    def keyword_overlap(self, job_text: str, resume_text: str) -> float:
        job_words = set(job_text.lower().split())
        res_words = set(resume_text.lower().split())
        if not job_words:
            return 0.0
        overlap = len(job_words.intersection(res_words))
        return round(overlap / len(job_words) * 100, 2)

    # -------------------------------------------------------
    # Utility: SAFE template formatting (no KeyError)
    # -------------------------------------------------------
    @staticmethod
    def _safe_format(template: str, **kwargs) -> str:
        """
        Try template.format(...). If the template has stray { } (e.g. JSON),
        fall back to leaving it untouched and appending the variables manually.
        """
        try:
            return template.format(**kwargs)
        except Exception as e:
            # Fallback: keep template literal and append context
            print(f"[WARN] Template .format() failed: {e}. Using fallback formatting.")
            parts = [template, "\n\n--- CONTEXT ---\n"]
            for k, v in kwargs.items():
                parts.append(f"\n[{k.upper()}]\n{v}\n")
            return "".join(parts)

    # -------------------------------------------------------
    # 1️⃣ Job Description Analysis (LLM)
    # -------------------------------------------------------
    def analyze_job_description(self, job_text: str) -> str:
        prompt_path = os.path.join(self.prompts_dir, "job_analysis.txt")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")

        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()

        # SAFE formatting
        prompt_text = self._safe_format(template, job_text=job_text)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()

    # -------------------------------------------------------
    # 2️⃣ Find Top-N Matches via FAISS
    # -------------------------------------------------------
    def find_top_matches(self, job_text: str, top_n: int = 3):
        index = self._load_index()
        id_map = self._load_id_map()

        query_vec = self.embed_text(job_text)
        distances, indices = index.search(query_vec, top_n)

        matches = []
        for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
            if 0 <= idx < len(id_map):
                matches.append({"rank": rank, "index": int(idx), "distance": float(dist)})

        print(f"[DEBUG] 🔍 Found {len(matches)} FAISS matches.")
        return matches

    # -------------------------------------------------------
    # 3️⃣ LLM Match Score + JSON Cleaning (ROBUST)
    # -------------------------------------------------------
    def llm_match_score(self, job_text: str, resume_text: str) -> dict:
        """
        Compare job and resume text using LLM reasoning.
        Always return a safe structured dictionary, even if LLM fails to produce proper JSON.
        """
        prompt_path = os.path.join(self.prompts_dir, "match_reasoning.txt")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")

        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()

        # SAFE formatting (no KeyError from stray { })
        prompt_text = self._safe_format(
            template,
            job_text=job_text,
            resume_text=resume_text
        )

        # Call LLM
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.2,
            )
            raw = response.choices[0].message.content.strip()
        except Exception as e:
            return {
                "MatchSummary": f"Error calling LLM: {str(e)}",
                "TechnicalSkills": [],
                "SoftSkills": [],
                "MissingSkills": [],
                "ExperienceAlignment": "",
                "MatchPercentage": 0.0,
            }

        # 🧹 Clean markdown fences
        cleaned = (
            raw.replace("```json", "")
            .replace("```", "")
            .replace("\n", " ")
            .strip()
        )

        # Try to parse JSON
        try:
            parsed = json.loads(cleaned)
            if not isinstance(parsed, dict):
                raise ValueError("Invalid JSON format")
        except Exception:
            parsed = {
                "MatchSummary": raw[:500],
                "TechnicalSkills": [],
                "SoftSkills": [],
                "MissingSkills": [],
                "ExperienceAlignment": "LLM returned non-JSON output.",
                "MatchPercentage": 0.0,
            }

        # Ensure mandatory keys exist
        defaults = {
            "MatchSummary": "",
            "TechnicalSkills": [],
            "SoftSkills": [],
            "MissingSkills": [],
            "ExperienceAlignment": "",
            "MatchPercentage": 0.0,
        }
        for k, v in defaults.items():
            if k not in parsed:
                parsed[k] = v

        # Normalize match percentage
        try:
            parsed["MatchPercentage"] = float(parsed.get("MatchPercentage", 0.0))
        except Exception:
            parsed["MatchPercentage"] = 0.0

        return parsed

    # -------------------------------------------------------
    # 4️⃣ Combine FAISS + LLM + Keyword Overlap
    # -------------------------------------------------------
    def ai_match_and_reason(self, job_text: str, top_n: int = 1):
        matches = self.find_top_matches(job_text, top_n)
        id_map = self._load_id_map()
        results = []

        for m in matches:
            idx = m["index"]
            resume_path = id_map[idx] if idx < len(id_map) else None
            if not resume_path or not os.path.exists(resume_path):
                continue

            resume_text = self.resume_agent.extract_text(resume_path)
            if not resume_text.strip():
                continue

            # Convert FAISS distance → similarity percentage
            faiss_sim = max(0.0, 1.0 - m["distance"])
            faiss_pct = round(faiss_sim * 100.0, 2)

            # Keyword and LLM scoring
            kw_pct = self.keyword_overlap(job_text, resume_text)
            llm_result = self.llm_match_score(job_text, resume_text)
            llm_pct = float(llm_result.get("MatchPercentage", 0.0))

            # Weighted average: 40% FAISS + 40% LLM + 20% Keyword
            final_pct = round(0.4 * faiss_pct + 0.4 * llm_pct + 0.2 * kw_pct, 2)

            print(
                f"[RESULT] {os.path.basename(resume_path)} → "
                f"FAISS={faiss_pct:.2f}% | KW={kw_pct:.2f}% | LLM={llm_pct:.2f}% "
                f"| FINAL={final_pct:.2f}%"
            )

            results.append({
                "rank": m["rank"],
                "distance": m["distance"],
                "faiss_similarity": faiss_pct,
                "keyword_overlap": kw_pct,
                "llm_score": llm_pct,
                "final_match_percentage": final_pct,
                "ai_reasoning": llm_result,
                "resume_path": resume_path,
            })

        print(f"[DEBUG] ✅ Completed matching for {len(results)} resumes.")
        return {"matches": results, "count": len(results)}

    # -------------------------------------------------------
    # 5️⃣ Full Pipeline → /analyze_match
    # -------------------------------------------------------
    def analyze_job(self, job_text: str, top_n: int = 1):
        try:
            job_analysis = self.analyze_job_description(job_text)
            match_results = self.ai_match_and_reason(job_text, top_n=top_n)

            return {
                "status": "success",
                "job_analysis": job_analysis,
                "match_results": match_results,
            }
        except Exception as e:
            return {"status": "error", "error": f"Job match pipeline failed: {str(e)}"}
