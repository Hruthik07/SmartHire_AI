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
│   ├── main.py                      # FastAPI application entry point
│   ├── agents/
│   │   ├── job_analyzer/           # Job analysis and matching logic
│   │   └── resume_analyzer/        # Resume text extraction and analysis
│   ├── models/                      # Pydantic models and schemas
│   ├── test/                        # Unit and integration tests
│   └── requirements.txt             # Python dependencies
│
├── frontend/
│   └── streamlit_app.py             # Streamlit UI application
│
├── data/
│   ├── resumes/                     # Uploaded resume files
│   ├── job_descriptions/            # Job description storage
│   └── embeddings/                  # FAISS index and metadata
│
├── .env.example                     # Environment configuration template
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── SECURITY.md                      # Security best practices
└── folder_structure.txt             # Detailed folder layout
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/Hruthik07/SmartHire_AI.git
cd SmartHire_AI
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Required: OPENAI_API_KEY=your_api_key_here
```

### 4. Prepare Data Directories

```bash
# Create necessary directories
mkdir -p data/resumes data/embeddings
```

### 5. Run the Backend

```bash
# Start the FastAPI server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### 6. Run the Frontend (in a new terminal)

```bash
# Activate virtual environment if not already active
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start Streamlit
streamlit run frontend/streamlit_app.py
```

The frontend will be available at `http://localhost:8501`

---

## 📖 Usage

1. **Upload Resume**: Use the sidebar to upload a PDF resume
2. **Enter Job Description**: Paste the job description in the main text area
3. **Analyze Match**: Click the "Analyze Match" button
4. **View Results**: Review the match score, skills analysis, and recommendations

---

## 🔒 Security

Please review [SECURITY.md](SECURITY.md) for important security considerations, especially before deploying to production.

Key security features:
- API key validation
- File upload restrictions (size, type)
- Input validation and sanitization
- Proper error handling without exposing sensitive information
- CORS configuration for production

---

## 🧪 Testing

```bash
# Run tests (when available)
pytest backend/test/

# Check for security vulnerabilities in dependencies
pip install safety
safety check
```

---

## 📊 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

- `GET /` - Health check
- `POST /analyze_resume` - Upload and extract text from resume
- `POST /analyze_match` - Analyze resume against job description

---

## 🛠️ Development

### Code Quality

The project follows these practices:
- Type hints for better code clarity
- Comprehensive logging
- Proper error handling
- Input validation
- Security best practices

### Logging

Logs are output to console with structured formatting. Configure log level via environment:
```bash
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

---

## 🐛 Troubleshooting

### Backend won't start
- Ensure `OPENAI_API_KEY` is set in `.env`
- Check all dependencies are installed: `pip install -r backend/requirements.txt`
- Verify port 8000 is not in use

### Frontend can't connect to backend
- Ensure backend is running on `http://localhost:8000`
- Check `BACKEND_URL` in `frontend/streamlit_app.py`

### Resume upload fails
- Check file size (max 10MB)
- Ensure file is PDF format
- Verify `data/resumes` directory exists

### Low match scores
- Ensure resume text is extractable (not scanned image)
- Check that FAISS embeddings are built (if using multi-resume mode)
- Verify job description is detailed and relevant

---

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**G D Hruthik**

---

## 🙏 Acknowledgments

- OpenAI for GPT and embedding models
- LangChain for LLM orchestration
- FastAPI for the web framework
- Streamlit for the UI framework
- FAISS for vector similarity search

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review [SECURITY.md](SECURITY.md) for security-related questions

---

**🚀 SmartHire AI v3.5** | Single-Resume Matching • FAISS + Keyword + GPT Reasoning
