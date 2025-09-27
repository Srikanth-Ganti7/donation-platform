#!/bin/bash
# Universal setup script for Unix-like systems (Linux, macOS)

echo "========================================"
echo " Donation Platform - First Time Setup"
echo "========================================"
echo

# Change to script directory
cd "$(dirname "$0")"

echo "1. Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "ERROR: Python is not installed!"
    echo "Please install Python 3.8 or later"
    exit 1
fi

$PYTHON_CMD --version
echo "✓ Python is installed"
echo

echo "2. Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    $PYTHON_CMD -m venv .venv
    echo "✓ Virtual environment created"
fi
echo

echo "3. Installing dependencies..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "ERROR: Virtual environment activation failed"
    exit 1
fi
echo

echo "4. Verifying installation..."
python -c "import fastapi; print('✓ FastAPI installed correctly')"
echo

echo "========================================"
echo " Setup Complete!"
echo "========================================"
echo
echo "You can now run the server using:"
echo "  ./run_server.sh"
echo
echo "Or activate the environment manually:"
echo "  source .venv/bin/activate"
echo "  python main.py"
echo
