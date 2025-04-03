#!/bin/bash
set -e

echo "Starting custom build process..."

# Set Python version
export PYTHONPATH="/vercel/path0:$PYTHONPATH"
python --version

# Create necessary directories
mkdir -p /tmp

# Install build dependencies first
echo "Installing build dependencies..."
pip install --upgrade pip setuptools wheel

# Install project dependencies
echo "Installing project requirements..."
pip install -r vercel-requirements.txt

echo "Build completed successfully" 