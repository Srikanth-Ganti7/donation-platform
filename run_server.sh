#!/bin/bash
# Universal run script for Unix-like systems (Linux, macOS)

echo "Starting Donation Platform API Server..."
echo

# Change to script directory
cd "$(dirname "$0")"

# Kill any existing processes on port 8000
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Stopping existing process on port 8000..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Check if virtual environment exists
if [ -f ".venv/bin/python" ]; then
    # Activate virtual environment and start server
    source .venv/bin/activate
    python main.py
else
    echo "ERROR: Virtual environment not found!"
    echo "Please run: ./setup.sh"
    exit 1
fi

echo
echo "Server stopped."
