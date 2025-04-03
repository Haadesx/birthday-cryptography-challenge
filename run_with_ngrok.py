from app import app
from pyngrok import ngrok
import os

# Open a ngrok tunnel to the HTTP server without auth (free, temporary, limited usage)
print("Starting ngrok tunnel (no auth token - limited to 1 hour / 40 connections per minute)")
public_url = ngrok.connect(5000)
print(f" * Running on {public_url}")
print(f" * Share this link with your friends: {public_url}")
print(" * NOTE: This link will expire when you close this script")

# Start the Flask app
if __name__ == '__main__':
    try:
        app.run(debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        # Clean up the ngrok tunnel
        ngrok.kill()
        print("Ngrok tunnel closed") 