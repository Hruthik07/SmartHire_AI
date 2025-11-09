"""
ResumeAnalyzerAgent
-------------------
Unified agent that can:
1️⃣  Extract and clean resume text from PDF files.
2️⃣  Analyze job descriptions using LLM.
3️⃣  Compute FAISS-based or cosine-based similarity between job & resume text.
4️⃣  Generate reasoning (why candidate fits).
"""

import os
import re
import numpy as np
import fitz  # PyMuPDF
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.agents.resume_analyzer.embeddings import get_embedding


class ResumeAnalyzerAgent:
    """
    Combines resume parsing, cleaning, similarity computation, and reasoning.
    """

    # ==========================================================
    # INIT
    # ==========================================================
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3)

    # ==========================================================
    # 1️⃣ RESUME TEXT EXTRACTION
    # ==========================================================
    def extract_text(self, pdf_path: str) -> str:
        """
        Extracts plain text from a PDF resume.
        """
        if not os.path.exists(pdf_path):
            print(f"[ResumeAnalyzerAgent] File not found: {pdf_path}")
            return ""

        text = ""
        try:
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    text += page.get_text("text")
        except Exception as e:
            print(f"[ResumeAnalyzerAgent] Error reading {pdf_path}: {e}")
        return text.strip()

    # ==========================================================
    # 2️⃣ TEXT CLEANING
    # ==========================================================
    def clean_text(self, text: str) -> str:
        """Basic cleaning for job description or resume text."""
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^a-zA-Z0-9,.\n@\- ]", "", text)
        return text.strip()

    # ==========================================================
    # 3️⃣ JOB DESCRIPTION ANALYSIS (LLM)
    # ==========================================================
    def analyze_job_description(self, job_text: str) -> str:
        """Extract structured info from job description."""
        prompt = ChatPromptTemplate.from_template("""
        You are an AI assistant that analyzes job descriptions.
        Extract structured JSON fields:
        - Job Title
        - Required Skills
        - Preferred Skills
        - Experience Level
        - Tools or Technologies
        - Short Summary (2 sentences max)
        Return valid JSON only.
        Job Description:
        {job_text}
        """)
        chain = prompt | self.llm
        response = chain.invoke({"job_text": job_text})
        return response.content

    # ==========================================================
    # 4️⃣ COSINE SIMILARITY (EMBEDDING-BASED)
    # ==========================================================
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts using embeddings."""
        emb1 = get_embedding(text1).astype("float32")
        emb2 = get_embedding(text2).astype("float32")
        num = np.dot(emb1, emb2)
        den = np.linalg.norm(emb1) * np.linalg.norm(emb2)
        return float(num / den) if den != 0 else 0.0

    # ==========================================================
    # 5️⃣ AI REASONING (LLM EXPLANATION)
    # ==========================================================
    def explain_match(self, job_text: str, resume_text: str, match_percent: float) -> str:
        """Generate natural-language reasoning for match results."""
        prompt = ChatPromptTemplate.from_template("""
        You are an AI recruiter assistant.
        Analyze how well this candidate matches the job.

        Job Description:
        {job_text}

        Candidate Resume:
        {resume_text}

        Current match score: {match_percent}%

        Explain clearly — mention key overlaps, strong skills, missing areas,
        and end with a concise summary.
        """)

        chain = prompt | self.llm
        response = chain.invoke({
            "job_text": job_text[:4000],
            "resume_text": resume_text[:4000],
            "match_percent": round(match_percent, 2)
        })
        return response.content.strip()

    # ==========================================================
    # 6️⃣ FULL PIPELINE
    # ==========================================================
    def match_resume_to_job(self, resume_text: str, job_text: str):
        """
        Full pipeline:
        - Clean both texts
        - Analyze job
        - Compute cosine similarity
        - Generate reasoning
        """
        cleaned_job = self.clean_text(job_text)
        cleaned_resume = self.clean_text(resume_text)

        # 1️⃣ Analyze job
        job_analysis = self.analyze_job_description(cleaned_job)

        # 2️⃣ Compute similarity
        similarity = self.compute_similarity(cleaned_job, cleaned_resume)
        match_percent = round(similarity * 100, 2)

        # 3️⃣ AI reasoning
        reasoning = self.explain_match(cleaned_job, cleaned_resume, match_percent)

        return {
            "status": "success",
            "match_percentage": match_percent,
            "ai_reasoning": reasoning,
            "job_analysis": job_analysis
        }
