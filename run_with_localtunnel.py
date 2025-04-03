import subprocess
import time
import sys
import webbrowser
import os

def main():
    print("Starting Birthday Cryptography Challenge App with localtunnel...")
    
    # Start Flask app in a separate process
    print("\n1. Starting Flask application...")
    if sys.platform == 'win32':
        flask_cmd = ["python", "app.py"]
    else:
        flask_cmd = ["python3", "app.py"]
        
    flask_process = subprocess.Popen(flask_cmd)
    
    # Wait for Flask to start
    print("   Waiting for Flask to initialize (5 seconds)...")
    time.sleep(5)
    
    # Start localtunnel in a separate process
    print("\n2. Creating public URL with localtunnel...")
    lt_cmd = ["npx", "localtunnel", "--port", "5000", "--subdomain", "birthdaycrypto"]
        
    lt_process = subprocess.Popen(lt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait for localtunnel to start and capture the URL
    print("   Setting up tunnel...")
    time.sleep(5)
    
    # Try to read output to get the URL
    public_url = None
    for line in lt_process.stdout:
        if "your url is:" in line.lower():
            public_url = line.strip().split("your url is: ")[1]
            break
    
    if not public_url:
        public_url = "https://birthdaycrypto.loca.lt"  # Default URL format for custom subdomain
    
    print(f"\n✅ Your application is now live at: {public_url}")
    print("   Share this URL with anyone to let them access your app!")
    print("\n   NOTE: This URL will only be active while this script is running.")
    print("   Press Ctrl+C to stop the server and close the tunnel.")
    
    # Optional: Open the URL in the default browser
    try:
        webbrowser.open(public_url)
        print("\n   Opening the URL in your default browser...")
    except:
        print("\n   Could not open browser automatically. Please manually open the URL.")
    
    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        # Clean up processes
        print("Terminating localtunnel...")
        lt_process.terminate()
        
        print("Shutting down Flask server...")
        flask_process.terminate()
        
        print("\nGoodbye! 👋")

if __name__ == "__main__":
    main() 