# Contributing to SmartHire AI

Thank you for your interest in contributing to SmartHire AI! This document provides guidelines and instructions for contributing to the project.

## 🌟 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Any relevant logs or screenshots

### Suggesting Enhancements

We welcome feature suggestions! Please create an issue with:
- Clear description of the enhancement
- Use case and benefits
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our code standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

## 🔧 Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- OpenAI API key

### Setup Steps

1. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/SmartHire_AI.git
cd SmartHire_AI
```

2. Run the setup script:
```bash
./setup.sh
```

3. Or manually set up:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
cp .env.example .env
# Edit .env with your API key
```

## 📝 Code Standards

### Python Style Guide

We follow PEP 8 with some modifications:
- Maximum line length: 100 characters
- Use type hints for function parameters and returns
- Write docstrings for all public functions and classes
- Use meaningful variable and function names

### Code Quality

- **Logging**: Use `logging` module, not `print()`
- **Error Handling**: Use specific exception types
- **Type Hints**: Add type hints to all functions
- **Docstrings**: Use Google-style docstrings

Example:
```python
def process_resume(file_path: str) -> Dict[str, Any]:
    """
    Process a resume file and extract information.
    
    Args:
        file_path: Path to the resume file
        
    Returns:
        Dict containing extracted resume data
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    pass
```

### Testing

- Write tests for new features
- Ensure existing tests pass
- Test error cases and edge cases

Run tests:
```bash
pytest backend/test/
```

### Security

- Never commit API keys or secrets
- Validate and sanitize all user inputs
- Use parameterized queries if database is added
- Follow security best practices in [SECURITY.md](SECURITY.md)

## 📋 Commit Message Guidelines

Use clear, descriptive commit messages:

- **feat**: New feature (e.g., "feat: add resume scoring algorithm")
- **fix**: Bug fix (e.g., "fix: handle empty resume files")
- **docs**: Documentation changes (e.g., "docs: update README setup instructions")
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

Example:
```
feat: add support for DOCX resume parsing

- Added python-docx dependency
- Implemented DOCX text extraction
- Updated tests and documentation
```

## 🔍 Code Review Process

All submissions require review. We aim to:
- Respond to PRs within 2-3 days
- Provide constructive feedback
- Help you improve your contribution

Reviewers will check:
- Code quality and standards
- Test coverage
- Documentation updates
- Security considerations
- Performance implications

## 🎯 Priority Areas

We especially welcome contributions in:
- Additional resume file format support
- Improved matching algorithms
- Better error handling
- Performance optimizations
- Documentation improvements
- Test coverage expansion
- UI/UX enhancements

## 📚 Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## ❓ Questions?

If you have questions:
- Check existing issues and discussions
- Create a new issue with the "question" label
- Reach out to maintainers

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on what's best for the community
- Show empathy towards others
- Accept constructive criticism gracefully

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other conduct inappropriate in a professional setting

## 🙏 Thank You!

Your contributions help make SmartHire AI better for everyone. We appreciate your time and effort!

---

**Questions or concerns?** Open an issue or contact the maintainers.
