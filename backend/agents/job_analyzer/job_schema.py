
"""
📘 JOB SCHEMA EXPLANATION
-------------------------
Why we created job_schema.py:
The JobSchema acts as a structured data model for every job description analyzed by SmartHire AI.
When the AI extracts information from a job post, the raw output from the LLM can be inconsistent or unstructured.
This schema ensures that all job data follows a fixed format, making it reliable and easy to use.

Why it’s important:
1️⃣ Validation – It validates AI output and ensures that required fields like job_title, skills, and technologies exist.
2️⃣ Consistency – Keeps data consistent for all agents (Job Analyzer, Matcher, Resume Builder, etc.).
3️⃣ Inter-Agent Communication – Acts as a shared data format between multiple agents in the SmartHire ecosystem.
4️⃣ Documentation – Automatically generates clear API structure when used with FastAPI or Swagger.
5️⃣ Scalability – Prepares the system for future database integration and analytics.

In simple words:
The JobSchema is the “grammar” of SmartHire AI’s job understanding system.
It keeps all AI agents speaking the same structured language, making the project cleaner, more accurate, and easier to expand.
"""


from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Union
import json

class JobSchema(BaseModel):
    """Structured representation of a job description extracted by SmartHire AI."""

    # Core job info
    job_title: str = Field(..., description="Official title of the job role")
    company: Optional[str] = Field(None, description="Name of the hiring company")
    location: Optional[str] = Field(None, description="City, state, or remote status")
    employment_type: Optional[str] = Field(None, description="Full-time, part-time, contract, or internship")
    seniority: Optional[str] = Field(None, description="Seniority level (Junior, Mid, Senior, Lead)")
    remote_policy: Optional[str] = Field(None, description="On-site, hybrid, or remote")
    salary: Optional[str] = Field(None, description="Mentioned salary range or note")

    # Compliance & HR info
    visa_sponsorship: Optional[bool] = Field(None, description="Whether visa sponsorship is available")
    work_auth_notes: Optional[str] = Field(None, description="Any notes about citizenship or work authorization")

    # Descriptive summary
    summary: Optional[str] = Field(None, description="Short summary of the role")
    responsibilities: List[str] = Field(default_factory=list, description="Main job responsibilities")

    # Skills and tools
    must_have_skills: List[str] = Field(default_factory=list, description="Essential skills required")
    nice_to_have_skills: List[str] = Field(default_factory=list, description="Preferred but non-essential skills")
    technologies: List[str] = Field(default_factory=list, description="Technical tools or software mentioned")
    keywords: List[str] = Field(default_factory=list, description="Extra relevant keywords for indexing")

    # Metadata
    posted_date: Optional[str] = Field(None, description="Date the job was posted")
    source_url: Optional[str] = Field(None, description="Original source or URL of the job post")

    # AI Matching extras
    suitability_score: Optional[float] = Field(None, description="Predicted suitability score by the AI matcher (0–1)")
    match_reasoning: Optional[str] = Field(None, description="Natural language reasoning for match results")

    @classmethod
    def from_text(cls, text: Union[str, dict]):
        """Parses raw LLM output (JSON string or dict) into a validated JobSchema object."""
        try:
            if isinstance(text, str):
                data = json.loads(text)
            else:
                data = text
            return cls(**data)
        except (ValidationError, json.JSONDecodeError) as e:
            raise ValueError(f"Invalid job schema format: {e}")

    class Config:
        schema_extra = {
            "example": {
                "job_title": "Machine Learning Engineer",
                "company": "Sanofi Boston",
                "location": "Cambridge, MA",
                "employment_type": "Full-time",
                "seniority": "Mid-level",
                "remote_policy": "Hybrid",
                "visa_sponsorship": True,
                "summary": "Responsible for developing and deploying ML models in biotech research.",
                "responsibilities": [
                    "Design and implement ML algorithms for biological datasets",
                    "Deploy production models using Docker and MLflow"
                ],
                "must_have_skills": ["Python", "TensorFlow", "MLflow", "Docker"],
                "nice_to_have_skills": ["Kubernetes", "AWS"],
                "technologies": ["Python", "TensorFlow", "Docker", "MLflow"],
                "keywords": ["AI", "Machine Learning", "Biotech"],
                "suitability_score": 0.87,
                "match_reasoning": "Strong ML and MLOps experience matching the biotech domain.",
                "work_auth_notes": "US Citizen or OPT/CPT allowed"
            }
        }
