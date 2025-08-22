#!/bin/bash

echo "=== PPTX Brand Restyler Setup ==="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

# Setup backend
echo "📦 Setting up backend..."
cd app/svc

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate fixtures
echo "🎨 Generating sample fixtures..."
python generate_fixtures.py

# Deactivate venv
deactivate

cd ../..

# Setup frontend
echo "📦 Setting up frontend..."
cd app/web
npm install

cd ../..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo ""
echo "Option 1: Using Docker Compose (recommended)"
echo "  cd app/infra"
echo "  docker-compose up --build"
echo ""
echo "Option 2: Run locally"
echo "  Terminal 1 (Backend):"
echo "    cd app/svc"
echo "    source venv/bin/activate"
echo "    uvicorn app.main:app --reload --port 8000"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd app/web"
echo "    npm run dev"
echo ""
echo "Access the application at http://localhost:3000"