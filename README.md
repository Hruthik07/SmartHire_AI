# 🧠 SmartHire AI — Intelligent Resume & Job Match Platform

SmartHire AI is an **AI-powered career assistant** that analyzes resumes, matches them with job descriptions, and generates optimized, recruiter-friendly resumes.  
The system integrates **LangChain, FAISS, FastAPI, Streamlit**, and a complete **MLOps pipeline** (DVC + MLflow + Docker + CI/CD).

---

## 🚀 Features

- 📄 **AI Resume Analyzer** — extracts and interprets skills, keywords, and experience using LLMs.  
- 🧩 **Job Description Matching Agent** — computes similarity between candidate resumes and job postings.  
- 📊 **Resume Score Evaluator** — provides a match-score and improvement suggestions.  
- 🧠 **LangChain + FAISS Integration** — enables retrieval-augmented generation (RAG) for contextual answers.  
- 🧰 **MLOps Infrastructure** — data versioning (DVC), experiment tracking (MLflow), and automated CI/CD pipelines.  
- 💻 **User-Friendly Frontend** — Streamlit interface for uploading resumes and viewing analytics.

---

## 🧱 Tech Stack

| Layer | Technologies |
|:------|:--------------|
| **Frontend** | Streamlit (UI) |
| **Backend API** | FastAPI + LangChain |
| **Vector DB** | FAISS |
| **LLM Embeddings** | OpenAI Embeddings / Hugging Face Models |
| **MLOps** | DVC · MLflow · Docker · GitHub Actions |
| **Deployment (Optional)** | Render / AWS EC2 / GCP / Azure |

---

## 🏗️ Folder Structure

```bash
SmartHire_AI/
│
├── backend/
│   ├── main.py
│   ├── routers/
│   ├── agents/
│   ├── utils/
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py
│   └── pages/
│       ├── resume_analysis.py
│       └── resume_builder.py
│
├── data/
│   ├── resumes/
│   ├── job_descriptions/
│   └── embeddings/
│
├── mlops/
│   ├── dvc.yaml
│   ├── params.yaml
│   ├── mlflow_experiments/
│   ├── Dockerfile
│   └── .github/workflows/ci_cd.yaml
│
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
