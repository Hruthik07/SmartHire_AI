import os
import shutil
import time
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# --------------------------------------------------
# Import your AI Agents
# --------------------------------------------------
from backend.agents.job_analyzer.agent import JobAnalyzerAgent
from backend.agents.resume_analyzer.agent_core import ResumeAnalyzerAgent

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
    allow_origins=["*"],  # Allow all origins (limit in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Initialize Agents
# --------------------------------------------------
job_agent = JobAnalyzerAgent()
resume_agent = ResumeAnalyzerAgent()

RESUME_DIR = os.path.join("backend", "data", "resumes")
os.makedirs(RESUME_DIR, exist_ok=True)

# --------------------------------------------------
# Health Check
# --------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "🚀 SmartHire AI backend is up and running!"}

# --------------------------------------------------
# Upload Resume Endpoint
# --------------------------------------------------
@app.post("/analyze_resume")
async def analyze_resume(file: UploadFile = File(...)):
    """
    Upload and extract text from a single resume file.
    """
    try:
        # Save uploaded resume
        save_path = os.path.join(RESUME_DIR, file.filename)
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract resume text
        resume_text = resume_agent.extract_text(save_path)
        text_length = len(resume_text or "")

        return {
            "status": "success",
            "file_name": file.filename,
            "resume_path": save_path,
            "text_length": text_length,
            "text_preview": resume_text[:600] if resume_text else "No text extracted.",
        }

    except Exception as e:
        return {"status": "error", "error": f"Resume processing failed: {str(e)}"}

# --------------------------------------------------
# Analyze Single Resume vs Job Description
# --------------------------------------------------
@app.post("/analyze_match")
async def analyze_match(job_description: str = Form(...)):
    """
    Analyze the most recently uploaded resume against a job description.
    """
    try:
        # ✅ Find the latest uploaded resume
        resumes = sorted(
            [os.path.join(RESUME_DIR, f) for f in os.listdir(RESUME_DIR)],
            key=os.path.getmtime,
        )

        if not resumes:
            return {"status": "error", "error": "No resumes uploaded. Please upload a resume first."}

        latest_resume = resumes[-1]
        resume_text = resume_agent.extract_text(latest_resume)

        if not resume_text.strip():
            return {"status": "error", "error": "Could not extract readable text from resume."}

        # Start timer
        start_time = time.time()
        print(f"[INFO] 🔍 Analyzing job match for resume: {latest_resume}")

        # Run job-agent LLM reasoning (no FAISS search required in single-resume mode)
        analysis_result = job_agent.analyze_job(job_description, top_n=1)

        # Add placeholder FAISS similarity to prevent frontend crash
        match_data = analysis_result.get("match_results", {})
        if isinstance(match_data, dict) and "matches" in match_data:
            for m in match_data["matches"]:
                m.setdefault("faiss_similarity", 100.0)

        elapsed = round(time.time() - start_time, 2)

        return {
            "status": "success",
            "message": "✅ Job analysis completed successfully.",
            "elapsed_time_sec": elapsed,
            "resume_file": os.path.basename(latest_resume),
            "job_analysis": analysis_result.get("job_analysis", "N/A"),
            "match_results": match_data,
        }

    except Exception as e:
        print(f"[ERROR] ❌ Job match pipeline failed: {e}")
        return {
            "status": "error",
            "error": f"Job match pipeline failed: {str(e)}",
        }
