import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("=" * 60)
    print("BIRTHDAY CRYPTOGRAPHY CHALLENGE APP LAUNCHER")
    print("=" * 60)
    print("\nThis script will start the Flask application on http://localhost:5000")
    print("\nTo expose this app to the internet, you have several options:")
    print("\n1. Use ngrok (requires signing up at https://ngrok.com):")
    print("   - Sign up for a free account at https://ngrok.com")
    print("   - Get your authtoken from the dashboard")
    print("   - Edit run_with_ngrok.py and add your authtoken")
    print("   - Run 'python run_with_ngrok.py'")
    
    print("\n2. Use a separate terminal to run:")
    print("   - If you have npm: 'npx localtunnel --port 5000'")
    print("   - If you have Go: 'cloudflared tunnel --url http://localhost:5000'")
    
    print("\nStarting the Flask application now...")
    
    # Start Flask app
    if sys.platform == 'win32':
        flask_cmd = ["python", "app.py"]
    else:
        flask_cmd = ["python3", "app.py"]
    
    # Open browser automatically after a short delay
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:5000")
        print("\nOpened application in browser!")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run Flask app (blocking call)
    try:
        subprocess.run(flask_cmd)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    
    print("\nApplication has been stopped.")

if __name__ == "__main__":
    main() 