#!/bin/bash

# Start script for Debate Room Chat Application
# This script starts both the backend server and frontend dev server

set -e

echo "================================================"
echo "  Debate Room Chat Application Startup"
echo "================================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with GEMINI_API_KEY"
    echo "Example: GEMINI_API_KEY='your_key_here'"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if Python dependencies are installed
echo "📦 Checking Python dependencies..."
if ! python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Check if frontend dependencies are installed
echo "📦 Checking frontend dependencies..."
if [ ! -d "debate-room-ui/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd debate-room-ui
    npm install
    cd ..
fi

echo ""
echo "✅ All dependencies installed"
echo ""

# Create a log directory
mkdir -p logs

# Start backend server
echo "🚀 Starting backend server..."
python3 debate_chat_server.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend server started (PID: $BACKEND_PID)"
echo "Backend logs: logs/backend.log"

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend failed to start! Check logs/backend.log"
    exit 1
fi

# Start frontend dev server
echo "🚀 Starting frontend dev server..."
cd debate-room-ui
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "Frontend server started (PID: $FRONTEND_PID)"
echo "Frontend logs: logs/frontend.log"

echo ""
echo "================================================"
echo "  ✅ Application Started Successfully!"
echo "================================================"
echo ""
echo "Backend API:  http://localhost:8080"
echo "Frontend UI:  http://localhost:5173"
echo ""
echo "To stop the application, press Ctrl+C or run:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Logs are available in the logs/ directory"
echo ""

# Save PIDs to a file for easy cleanup
echo "$BACKEND_PID" > logs/backend.pid
echo "$FRONTEND_PID" > logs/frontend.pid

# Wait for user to stop
echo "Press Ctrl+C to stop all servers..."
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Servers stopped.'; exit 0" INT TERM

# Keep script running
wait
