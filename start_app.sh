#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Function to handle script termination
cleanup() {
    echo "Stopping all services..."
    jobs -p | xargs -r kill
    exit
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

echo "Starting Gmail Tracking Dashboard..."

# 1. Start Backend
echo ">> Starting Backend..."
cd "$BACKEND_DIR"
# Ensure local env file exists.
if [ ! -f ".env" ]; then
    echo "Creating backend/.env from example..."
    cp .env.example .env
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found in backend/. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

BACKEND_PYTHON="$BACKEND_DIR/venv/bin/python"

if [ ! -f "credentials.json" ]; then
    echo "Missing backend/credentials.json."
    echo "Download your OAuth client JSON from Google Cloud and place it at:"
    echo "  $BACKEND_DIR/credentials.json"
    echo "See CREDENTIALS_HELP.md for the exact steps."
    exit 1
fi

# Run Migrations
echo ">> Running Database Migrations..."
"$BACKEND_PYTHON" migrate_db.py

# Start FastApi
echo ">> Launching API Server..."
"$BACKEND_PYTHON" -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# 2. Start Frontend
echo ">> Starting Frontend..."
cd "$FRONTEND_DIR"
# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Node modules not found. Installing..."
    npm install
fi
echo ">> Launching UI..."
npm run dev -- --host &
FRONTEND_PID=$!
cd ..

echo "------------------------------------------------"
echo "Gmail Dashboard is running!"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "------------------------------------------------"
echo "Press Ctrl+C to stop."

# Wait for all background processes
wait
