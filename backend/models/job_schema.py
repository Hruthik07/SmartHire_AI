# backend/models/job_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional

class JobSpec(BaseModel):
    job_title: str = Field(..., description="Official title of the job role")
    company: Optional[str] = Field(None, description="Name of the hiring company")
    location: Optional[str] = Field(None, description="City, state, or remote status")
    employment_type: Optional[str] = Field(None, description="Full-time, part-time, contract, or internship")
    seniority: Optional[str] = Field(None, description="Seniority level (Junior, Mid, Senior, Lead)")
    remote_policy: Optional[str] = Field(None, description="On-site, hybrid, or remote")
    visa_sponsorship: Optional[bool] = Field(None, description="Whether visa sponsorship is available")
    work_auth_notes: Optional[str] = Field(None, description="Any notes about citizenship or work authorization")
    salary: Optional[str] = Field(None, description="Mentioned salary range or note")
    summary: Optional[str] = Field(None, description="Short summary of the role")
    responsibilities: List[str] = Field(default_factory=list, description="Main job responsibilities")
    must_have_skills: List[str] = Field(default_factory=list, description="Essential skills required")
    nice_to_have_skills: List[str] = Field(default_factory=list, description="Preferred but non-essential skills")
    technologies: List[str] = Field(default_factory=list, description="Technical tools or software mentioned")
    keywords: List[str] = Field(default_factory=list, description="Extra relevant keywords for indexing")
    posted_date: Optional[str] = Field(None, description="Date the job was posted")
    source_url: Optional[str] = Field(None, description="Original source or URL of the job post")

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
                "work_auth_notes": "US Citizen or OPT/CPT allowed"
            }
        }
