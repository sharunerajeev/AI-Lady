#!/bin/bash

# AI Insurance Assistant - Startup Script

set -e

echo "🚀 Starting AI Insurance Assistant..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✓ Created .env file. Please configure your AI provider settings."
    echo ""
    read -p "Press Enter to continue with default settings or Ctrl+C to exit and configure..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create necessary directories
mkdir -p logs

echo ""
echo "✅ Setup complete!"
echo ""

# Start the application
echo "🌐 Starting FastAPI server..."
echo ""
echo "📍 Access points:"
echo "   - Web UI:     http://localhost:8000/static/index.html"
echo "   - API Docs:   http://localhost:8000/docs"
echo "   - Health:     http://localhost:8000/api/v1/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py
