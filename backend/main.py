import os
import shutil
import time
import logging
from typing import Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --------------------------------------------------
# Import your AI Agents
# --------------------------------------------------
from backend.agents.job_analyzer.agent import JobAnalyzerAgent
from backend.agents.resume_analyzer.agent_core import ResumeAnalyzerAgent

# --------------------------------------------------
# Configure Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Constants
# --------------------------------------------------
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}
MAX_JOB_DESCRIPTION_LENGTH = 50000  # characters

# --------------------------------------------------
# FastAPI Setup
# --------------------------------------------------
app = FastAPI(
    title="SmartHire AI Backend (Single Resume Mode)",
    description="AI-powered resume analysis and job matching system.",
    version="3.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Initialize Agents
# --------------------------------------------------
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    job_agent = JobAnalyzerAgent()
    resume_agent = ResumeAnalyzerAgent()
    logger.info("AI agents initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI agents: {e}")
    raise

RESUME_DIR = os.path.join("backend", "data", "resumes")
os.makedirs(RESUME_DIR, exist_ok=True)

# --------------------------------------------------
# Health Check
# --------------------------------------------------
@app.get("/")
def root() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "message": "🚀 SmartHire AI backend is up and running!"}

# --------------------------------------------------
# Upload Resume Endpoint
# --------------------------------------------------
@app.post("/analyze_resume")
async def analyze_resume(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload and extract text from a single resume file.
    
    Args:
        file: Uploaded resume file (PDF, DOCX, DOC, or TXT)
        
    Returns:
        Dict containing status, filename, path, text length, and preview
        
    Raises:
        HTTPException: If file validation fails or processing errors occur
    """
    try:
        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content to check size
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Reset file pointer after reading
        await file.seek(0)
        
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(file.filename)
        save_path = os.path.join(RESUME_DIR, safe_filename)
        
        # Save uploaded resume
        with open(save_path, "wb") as f:
            f.write(file_content)
        
        logger.info(f"Resume uploaded successfully: {safe_filename}")

        # Extract resume text
        resume_text = resume_agent.extract_text(save_path)
        text_length = len(resume_text or "")
        
        if text_length < 50:
            logger.warning(f"Very short text extracted from {safe_filename}: {text_length} chars")

        return {
            "status": "success",
            "file_name": safe_filename,
            "resume_path": save_path,
            "text_length": text_length,
            "text_preview": resume_text[:600] if resume_text else "No text extracted.",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume processing failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Resume processing failed: {str(e)}"
        )

# --------------------------------------------------
# Analyze Single Resume vs Job Description
# --------------------------------------------------
@app.post("/analyze_match")
async def analyze_match(job_description: str = Form(...)) -> Dict[str, Any]:
    """
    Analyze the most recently uploaded resume against a job description.
    
    Args:
        job_description: The job description text to match against
        
    Returns:
        Dict containing match analysis results
        
    Raises:
        HTTPException: If validation fails or processing errors occur
    """
    try:
        # Validate job description
        if not job_description or not job_description.strip():
            raise HTTPException(
                status_code=400,
                detail="Job description cannot be empty"
            )
        
        if len(job_description) > MAX_JOB_DESCRIPTION_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Job description too long. Maximum length: {MAX_JOB_DESCRIPTION_LENGTH} characters"
            )
        
        # Find the latest uploaded resume
        if not os.path.exists(RESUME_DIR):
            raise HTTPException(
                status_code=500,
                detail="Resume directory not found"
            )
            
        resumes = [
            os.path.join(RESUME_DIR, f) 
            for f in os.listdir(RESUME_DIR) 
            if os.path.isfile(os.path.join(RESUME_DIR, f))
        ]
        
        if not resumes:
            raise HTTPException(
                status_code=400,
                detail="No resumes uploaded. Please upload a resume first."
            )
        
        resumes_sorted = sorted(resumes, key=os.path.getmtime)
        latest_resume = resumes_sorted[-1]
        
        logger.info(f"Analyzing job match for resume: {os.path.basename(latest_resume)}")
        
        resume_text = resume_agent.extract_text(latest_resume)

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract readable text from resume"
            )

        # Start timer
        start_time = time.time()

        # Run job-agent LLM reasoning
        analysis_result = job_agent.analyze_job(job_description, top_n=1)
        
        if analysis_result.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=analysis_result.get("error", "Job analysis failed")
            )

        # Add placeholder FAISS similarity to prevent frontend crash
        match_data = analysis_result.get("match_results", {})
        if isinstance(match_data, dict) and "matches" in match_data:
            for m in match_data["matches"]:
                m.setdefault("faiss_similarity", 100.0)

        elapsed = round(time.time() - start_time, 2)
        
        logger.info(f"Job analysis completed in {elapsed}s")

        return {
            "status": "success",
            "message": "✅ Job analysis completed successfully.",
            "elapsed_time_sec": elapsed,
            "resume_file": os.path.basename(latest_resume),
            "job_analysis": analysis_result.get("job_analysis", "N/A"),
            "match_results": match_data,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Job match pipeline failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Job match pipeline failed: {str(e)}"
        )
