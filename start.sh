#!/bin/bash
# Quick start script for QuantumShield Simulator

echo "🔐 QuantumShield - Frontend/Backend Crypto Simulation"
echo "=================================================="
echo ""

# Navigate to project
cd /home/shiva/PQC-POC

# Check if virtual environment exists
if [ ! -d "venv_simulator" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv_simulator
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv_simulator/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q flask flask-cors pycryptodome liboqs-python requests 2>/dev/null

# Set environment variables for liboqs
export OQS_INSTALL_DIR=$HOME/.local
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH

echo ""
echo "✓ Environment Ready!"
echo ""
echo "Choose an option:"
echo "  1) Start Web Interface (http://localhost:5000)"
echo "  2) Run Command-line Test"
echo "  3) Exit"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting Flask server..."
        echo "Web UI will be available at: http://localhost:5000"
        echo ""
        python3 app.py
        ;;
    2)
        echo ""
        echo "Running encryption/decryption test..."
        python3 test_simulation.py
        ;;
    3)
        echo "Goodbye!"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
