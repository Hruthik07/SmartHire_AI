#!/bin/bash

# SmartHire AI Quick Start Script
# This script helps you set up and run the SmartHire AI application

set -e  # Exit on error

echo "🧠 SmartHire AI - Quick Start"
echo "=============================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r backend/requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    if [ -f ".env.example" ]; then
        echo "Would you like to copy .env.example to .env? (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            cp .env.example .env
            echo "✓ Created .env file from .env.example"
            echo ""
            echo "⚠️  IMPORTANT: Please edit .env and add your OPENAI_API_KEY"
            echo "   Open .env in a text editor and replace 'your_openai_api_key_here'"
            echo ""
        else
            echo "Please create a .env file with your OPENAI_API_KEY before running the application"
            exit 1
        fi
    else
        echo "Please create a .env file with your OPENAI_API_KEY"
        exit 1
    fi
else
    echo "✓ .env file found"
fi
echo ""

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/resumes data/embeddings
echo "✓ Data directories created"
echo ""

echo "=============================="
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend (in this terminal):"
echo "   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. Start the frontend (in a new terminal):"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   streamlit run frontend/streamlit_app.py"
echo ""
echo "3. Open your browser to http://localhost:8501"
echo ""
echo "=============================="
