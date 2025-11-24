"""
Embeddings Manager
------------------
Handles creation, loading, and management of FAISS embeddings
for all resumes in data/resumes. Keeps a resume_ids.json mapping
to preserve link between FAISS vectors and actual files.
"""

import os
import json
import logging
import numpy as np
import faiss
from pathlib import Path
from typing import Optional, List
from langchain_openai import OpenAIEmbeddings

# Configure logging
logger = logging.getLogger(__name__)

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
try:
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    logger.info("OpenAI embedding model initialized")
except Exception as e:
    logger.error(f"Failed to initialize embedding model: {e}")
    raise


def get_embedding(text: str) -> np.ndarray:
    """
    Generate embedding vector for a given text.
    
    Args:
        text: Input text to embed
        
    Returns:
        Numpy array of embedding vector
    """
    if not text or not text.strip():
        logger.warning("Attempting to embed empty text")
        return np.zeros((1536,), dtype="float32")
    
    try:
        vec = embedding_model.embed_query(text)
        return np.array(vec, dtype="float32")
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        return np.zeros((1536,), dtype="float32")  # fallback shape


# ==========================================================
# ✅ INDEX SAVE / LOAD HELPERS
# ==========================================================
def save_index(index: faiss.Index, id_map: List[str]) -> None:
    """
    Save FAISS index and its corresponding ID mapping.
    
    Args:
        index: FAISS index to save
        id_map: List of resume file paths corresponding to index
    """
    try:
        faiss.write_index(index, str(INDEX_PATH))
        with open(IDS_PATH, "w", encoding="utf-8") as f:
            json.dump(id_map, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved FAISS index for {len(id_map)} resumes")
    except Exception as e:
        logger.error(f"Failed to save FAISS index: {e}")
        raise


def load_index() -> Optional[faiss.Index]:
    """
    Load FAISS index if available.
    
    Returns:
        FAISS index or None if not found
    """
    if not INDEX_PATH.exists():
        logger.info("No FAISS index found")
        return None
    try:
        index = faiss.read_index(str(INDEX_PATH))
        logger.debug(f"Loaded FAISS index from {INDEX_PATH}")
        return index
    except Exception as e:
        logger.error(f"Failed to load FAISS index: {e}")
        return None


def load_id_map() -> Optional[List[str]]:
    """
    Load resume ID map (maps FAISS vector → file path).
    
    Returns:
        List of resume paths or None if not found
    """
    if not IDS_PATH.exists():
        logger.info("No resume ID map found")
        return None
    try:
        with open(IDS_PATH, "r", encoding="utf-8") as f:
            id_map = json.load(f)
        logger.debug(f"Loaded ID map with {len(id_map)} entries")
        return id_map
    except Exception as e:
        logger.error(f"Failed to load resume_ids.json: {e}")
        return None


# ==========================================================
# ✅ INDEX REBUILD (Renamed to match main.py → rebuild_embeddings)
# ==========================================================
def rebuild_embeddings() -> None:
    """
    Rebuild FAISS index from all resumes in data/resumes folder.
    
    Raises:
        FileNotFoundError: If resume folder doesn't exist
        ValueError: If no valid resumes found
    """
    from backend.agents.resume_analyzer.agent_core import ResumeAnalyzerAgent

    if not RESUME_DIR.exists():
        raise FileNotFoundError(f"Resume folder not found: {RESUME_DIR}")

    resume_agent = ResumeAnalyzerAgent()
    embeddings, paths = [], []

    logger.info(f"Scanning resumes in {RESUME_DIR}")
    
    for file in sorted(RESUME_DIR.iterdir()):
        if file.is_file():
            try:
                text = resume_agent.extract_text(str(file)).strip()
                if not text:
                    logger.warning(f"Skipped empty file: {file.name}")
                    continue

                emb = get_embedding(text)
                embeddings.append(emb)
                paths.append(str(file.resolve()))
                logger.debug(f"Processed: {file.name}")
            except Exception as e:
                logger.error(f"Failed to process {file.name}: {e}")
                continue

    if not embeddings:
        raise ValueError("No valid resumes found to embed")

    matrix = np.vstack(embeddings).astype("float32")
    index = faiss.IndexFlatL2(matrix.shape[1])
    index.add(matrix)

    save_index(index, paths)
    logger.info(f"Rebuilt FAISS index with {len(paths)} resumes")


# ==========================================================
# ✅ DEBUG MODE
# ==========================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Running standalone FAISS rebuild...")
    logger.debug(f"PROJECT_ROOT: {PROJECT_ROOT}")
    logger.debug(f"DATA_DIR: {DATA_DIR}")
    logger.debug(f"EMBED_DIR: {EMBED_DIR}")
    logger.debug(f"RESUME_DIR: {RESUME_DIR}")
    rebuild_embeddings()
