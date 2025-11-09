"""
Embeddings Manager
------------------
Handles creation, loading, and management of FAISS embeddings
for all resumes in data/resumes. Keeps a resume_ids.json mapping
to preserve link between FAISS vectors and actual files.
"""

import os
import json
import numpy as np
import faiss
from pathlib import Path
from langchain_openai import OpenAIEmbeddings

# ==========================================================
# ✅ PATH SETUP (Correct for your structure)
# ==========================================================
# Example: C:/SmartHire_AI/backend/agents/resume_analyzer/embeddings.py
# We go up 3 levels → C:/SmartHire_AI (project root)
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Data folder exists directly under project root
DATA_DIR = PROJECT_ROOT / "data"
RESUME_DIR = DATA_DIR / "resumes"
EMBED_DIR = DATA_DIR / "embeddings"

# Ensure embedding directory exists
EMBED_DIR.mkdir(parents=True, exist_ok=True)

# Paths for FAISS index and ID mapping
INDEX_PATH = EMBED_DIR / "resume_faiss.index"
IDS_PATH = EMBED_DIR / "resume_ids.json"


# ==========================================================
# ✅ EMBEDDING MODEL
# ==========================================================
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


def get_embedding(text: str) -> np.ndarray:
    """Generate embedding vector for a given text."""
    try:
        vec = embedding_model.embed_query(text)
        return np.array(vec, dtype="float32")
    except Exception as e:
        print(f"[ERROR] Embedding generation failed: {e}")
        return np.zeros((1536,), dtype="float32")  # fallback shape


# ==========================================================
# ✅ INDEX SAVE / LOAD HELPERS
# ==========================================================
def save_index(index, id_map):
    """Save FAISS index and its corresponding ID mapping."""
    faiss.write_index(index, str(INDEX_PATH))
    with open(IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(id_map, f, ensure_ascii=False, indent=2)
    print(f"[OK] ✅ Saved FAISS index for {len(id_map)} resumes.")


def load_index():
    """Load FAISS index if available."""
    if not INDEX_PATH.exists():
        print("[INFO] No FAISS index found.")
        return None
    try:
        return faiss.read_index(str(INDEX_PATH))
    except Exception as e:
        print(f"[ERROR] Failed to load FAISS index: {e}")
        return None


def load_id_map():
    """Load resume ID map (maps FAISS vector → file path)."""
    if not IDS_PATH.exists():
        print("[INFO] No resume ID map found.")
        return None
    try:
        with open(IDS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load resume_ids.json: {e}")
        return None


# ==========================================================
# ✅ INDEX REBUILD (Renamed to match main.py → rebuild_embeddings)
# ==========================================================
def rebuild_embeddings():
    """
    Rebuild FAISS index from all resumes in data/resumes folder.
    """
    from backend.agents.resume_analyzer.agent_core import ResumeAnalyzerAgent

    if not RESUME_DIR.exists():
        raise FileNotFoundError(f"Resume folder not found: {RESUME_DIR}")

    resume_agent = ResumeAnalyzerAgent()
    embeddings, paths = [], []

    for file in sorted(RESUME_DIR.iterdir()):
        if file.is_file():
            text = resume_agent.extract_text(str(file)).strip()
            if not text:
                print(f"[WARN] ⚠️ Skipped empty file: {file.name}")
                continue

            emb = get_embedding(text)
            embeddings.append(emb)
            paths.append(str(file.resolve()))

    if not embeddings:
        raise ValueError("No valid resumes found to embed.")

    matrix = np.vstack(embeddings).astype("float32")
    index = faiss.IndexFlatL2(matrix.shape[1])
    index.add(matrix)

    save_index(index, paths)
    print(f"[OK] ✅ Rebuilt FAISS index with {len(paths)} resumes.")


# ==========================================================
# ✅ DEBUG MODE
# ==========================================================
if __name__ == "__main__":
    print("[DEBUG] Running standalone FAISS rebuild...")
    print(f"[DEBUG] PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"[DEBUG] DATA_DIR: {DATA_DIR}")
    print(f"[DEBUG] EMBED_DIR: {EMBED_DIR}")
    print(f"[DEBUG] RESUME_DIR: {RESUME_DIR}")
    rebuild_embeddings()
