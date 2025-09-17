#!/bin/bash

# GemmaSOS Installation Script
# Installs dependencies and sets up the crisis intervention system

set -e

echo "🔒 GemmaSOS - Crisis Intervention System Installation"
echo "=================================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version detected (requires 3.8+)"
else
    echo "❌ Python 3.8+ required. Found: $python_version"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p temp

# Set permissions
echo "Setting permissions..."
chmod +x run.py
chmod +x test_system.py

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "To run the system:"
echo "  python run.py"
echo ""
echo "To test the system:"
echo "  python test_system.py"
echo ""
echo "To activate the virtual environment manually:"
echo "  source venv/bin/activate"
echo ""
echo "🔒 Privacy Notice: All processing happens on your device."
echo "   No data is sent to external servers."
