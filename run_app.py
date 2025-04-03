#!/usr/bin/env python3
import os
import sys
import subprocess

def check_dependencies():
    """Check if all required modules are installed."""
    try:
        import flask
        import cryptography
        import cv2
        import numpy
        print("✓ All required dependencies are installed.")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease install all required packages:")
        print("pip install -r requirements_web.txt")
        return False

def check_templates():
    """Check if template directory exists and contains required files."""
    if not os.path.isdir("templates"):
        print("✗ 'templates' directory not found!")
        return False
    
    required_templates = ["base.html", "index.html", "encryption.html", "steganography.html", "challenge.html"]
    missing = []
    
    for template in required_templates:
        if not os.path.exists(os.path.join("templates", template)):
            missing.append(template)
    
    if missing:
        print(f"✗ Missing templates: {', '.join(missing)}")
        return False
    else:
        print("✓ All required templates are present.")
        return True

def check_uploads_dir():
    """Check if uploads directory exists and is writable."""
    if not os.path.isdir("uploads"):
        try:
            os.mkdir("uploads")
            print("✓ Created 'uploads' directory.")
        except PermissionError:
            print("✗ Cannot create 'uploads' directory. Permission denied.")
            return False
    
    # Check if directory is writable
    try:
        test_file = os.path.join("uploads", "test_write.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print("✓ 'uploads' directory is writable.")
        return True
    except PermissionError:
        print("✗ 'uploads' directory is not writable.")
        return False

def run_app():
    """Run the Flask application."""
    if sys.platform == "win32":
        print("\nStarting Flask application...\n")
        subprocess.run(["python", "app.py"])
    else:
        print("\nStarting Flask application...\n")
        subprocess.run(["python3", "app.py"])

if __name__ == "__main__":
    print("\n====== Birthday Cryptography Web App Checker ======\n")
    
    dependencies_ok = check_dependencies()
    templates_ok = check_templates()
    uploads_ok = check_uploads_dir()
    
    if dependencies_ok and templates_ok and uploads_ok:
        print("\n✓ All checks passed! The application is ready to run.")
        
        while True:
            choice = input("\nDo you want to start the application now? (y/n): ").lower()
            if choice == 'y':
                run_app()
                break
            elif choice == 'n':
                print("\nYou can start the application later by running:")
                print("python app.py")
                break
            else:
                print("Please enter 'y' or 'n'.")
    else:
        print("\n✗ Some checks failed. Please fix the issues and try again.") 