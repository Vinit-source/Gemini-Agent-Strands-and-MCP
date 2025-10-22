#!/bin/bash

# Stop script for Debate Room Chat Application

echo "Stopping Debate Room Chat Application..."

# Check for PID files
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "Stopping backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
    fi
    rm logs/backend.pid
fi

if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "Stopping frontend server (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
    fi
    rm logs/frontend.pid
fi

# Also kill any lingering processes
pkill -f "debate_chat_server.py" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo "✅ Servers stopped"
