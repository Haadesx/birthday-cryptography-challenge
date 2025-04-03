# Birthday Cryptography Challenge

A special birthday gift that combines Python, cryptography, and steganography in an interactive web application.

## Features

- **Interactive Cryptography Challenges**: 
  - Caesar Cipher
  - Vigenère Cipher 
  - Base64 Decoding
- **Celebration Effects**: Confetti animation when all challenges are completed
- **Progress Tracking**: Visual indicators for completed challenges
- **Responsive Design**: Works on both desktop and mobile devices

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Flask

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/birthday-cryptography-challenge.git
   cd birthday-cryptography-challenge
   ```

2. Install the requirements:
   ```
   pip install -r requirements_web.txt
   ```

3. Run the application:
   ```
   python run_app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

- `app.py`: Main Flask application
- `run_app.py`: Script to start the application
- `templates/`: HTML templates for the web interface
- `static/`: CSS, JS, and image files
- `requirements_web.txt`: Python dependencies
- `fixes_notes.md`: Development notes and bug tracking

## Customization

You can customize the messages, ciphers, and challenges by modifying:

- `app.py`: Contains the cryptography functions
- `templates/all_challenges.html`: Contains the challenge content and verification logic

## Deployment

The application is designed to be deployable on platforms like:
- Heroku
- Render
- PythonAnywhere
- Vercel with a WSGI server

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with Flask, Bootstrap, and JavaScript
- Inspired by classical cryptography techniques 