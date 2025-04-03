from app import app
import subprocess
import webbrowser
import time

if __name__ == '__main__':
    # Start Flask app in a separate process
    flask_process = subprocess.Popen(["python", "app.py"])
    
    # Wait for the Flask app to start
    print("Waiting for Flask app to start...")
    time.sleep(5)
    
    try:
        # Start tunnel in a separate process
        print("Starting tunnel to expose the app...")
        tunnel_process = subprocess.Popen(["tunnel", "5000"])
        
        # Open the browser to the app
        print("The app should now be accessible via the tunnel URL shown above.")
        print("Press Ctrl+C to stop the app and tunnel")
        
        # Keep the script running until user interrupts
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Clean up processes
        print("Terminating tunnel and Flask app...")
        if 'tunnel_process' in locals():
            tunnel_process.terminate()
        if 'flask_process' in locals():
            flask_process.terminate()
        print("Done.") 