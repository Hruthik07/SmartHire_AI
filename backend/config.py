"""
Configuration module for SmartHire AI Backend
Centralizes all configuration settings and constants
"""

import os
from typing import Set
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================================
# API Configuration
# ==========================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# ==========================================================
# CORS Configuration
# ==========================================================
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")

# ==========================================================
# File Upload Configuration
# ==========================================================
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".doc", ".txt"}

# ==========================================================
# Input Validation Configuration
# ==========================================================
MAX_JOB_DESCRIPTION_LENGTH = 50000  # characters
MIN_RESUME_TEXT_LENGTH = 50  # characters

# ==========================================================
# Directory Configuration
# ==========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESUME_DIR = os.path.join(DATA_DIR, "resumes")
EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")

# Create directories if they don't exist
os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

# ==========================================================
# Model Configuration
# ==========================================================
LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_TEMPERATURE = 0.2
LLM_TIMEOUT = 60  # seconds

# ==========================================================
# Matching Algorithm Configuration
# ==========================================================
# Weights for final match score calculation
WEIGHT_FAISS = 0.4
WEIGHT_LLM = 0.4
WEIGHT_KEYWORD = 0.2

# ==========================================================
# Logging Configuration
# ==========================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==========================================================
# API Configuration
# ==========================================================
API_TITLE = "SmartHire AI Backend"
API_DESCRIPTION = "AI-powered resume analysis and job matching system."
API_VERSION = "3.5.0"
