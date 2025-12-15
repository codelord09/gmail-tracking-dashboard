#!/bin/bash

# Function to handle script termination
cleanup() {
    echo "Stopping all services..."
    kill $(jobs -p)
    exit
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

echo "Starting Gmail Tracking Dashboard..."

# 1. Start Backend
echo ">> Starting Backend..."
cd backend
# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found in backend/. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run Migrations
echo ">> Running Database Migrations..."
python migrate_db.py

# Start FastApi
echo ">> Launching API Server..."
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# 2. Start Frontend
echo ">> Starting Frontend..."
cd frontend
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
