# Changelog

All notable changes to SmartHire AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.5.0] - 2024-11-24

### Added
- Centralized configuration module (`backend/config.py`) for all settings
- Comprehensive security documentation (`SECURITY.md`)
- Environment configuration template (`.env.example`)
- Detailed setup instructions in README
- Troubleshooting guide in README
- Quick start setup script (`setup.sh`)
- Contributing guidelines (`CONTRIBUTING.md`)
- Utility functions module (`backend/utils.py`)
- Type hints throughout the codebase
- Comprehensive docstrings for all public methods
- UUID-based unique filename generation for uploads

### Changed
- Replaced all `print()` statements with structured logging
- Updated CORS configuration to use environment variables
- Improved error handling with specific exception types (HTTPException)
- Enhanced frontend error handling (timeouts, connection errors)
- API key validation moved to application startup
- Match scoring weights now use centralized configuration
- LLM timeout and temperature configurable via constants

### Fixed
- Security: CORS now uses environment-specific allowed origins (not `*`)
- Security: Added file upload validation (size, type, sanitization)
- Security: Fixed filename collision vulnerability
- Fixed import path inconsistency (agent.py vs agent_core.py)
- Fixed typo in match_reasoning.txt prompt ("Yyou" → "You")
- Improved error messages to be user-friendly
- Added proper HTTP status code handling in frontend

### Security
- Added comprehensive input validation
- File size limits enforced (10MB max)
- File type restrictions (PDF, DOCX, DOC, TXT only)
- Filename sanitization to prevent path traversal
- API key validation at startup
- Proper error handling without exposing sensitive information

## [3.2.0] - Previous Version

### Features
- Single-resume matching mode
- FAISS vector similarity search
- Keyword overlap analysis
- LLM-powered reasoning and scoring
- FastAPI backend with OpenAI integration
- Streamlit frontend UI
- Resume text extraction (PDF, DOCX, TXT)
- Job description analysis
- Match score visualization

---

## Version History

### Version Format
- **Major.Minor.Patch** (e.g., 3.5.0)
- **Major**: Breaking changes
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes, backwards compatible

### Categories
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements
