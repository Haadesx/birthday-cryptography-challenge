#!/usr/bin/env python
import os
import sys
import subprocess

# Force Python 3.9
print("Vercel prebuild script running...")
print(f"Python version: {sys.version}")

# Create necessary directories
os.makedirs("/tmp", exist_ok=True)

# Install build requirements
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
print("Build dependencies installed successfully")

# Check that OpenCV dependencies are available
try:
    import numpy
    print(f"NumPy version: {numpy.__version__}")
except ImportError:
    print("Installing NumPy...")
    subprocess.run([sys.executable, "-m", "pip", "install", "numpy==1.24.2"])

print("Prebuild script completed successfully") 