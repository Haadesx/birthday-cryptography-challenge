# Birthday Cryptography Web Application for Lisa

A special birthday gift for Lisa Menpara combining Python, cryptography, and steganography in a web application.

## Features

- Modern encryption/decryption using Fernet
- Classical ciphers (Caesar and Vigenère)
- Message hashing with multiple algorithms
- Steganography for hiding messages in images
- Interactive birthday cryptography challenge

## Local Development

1. Install the required packages:

```bash
pip install -r requirements_web.txt
```

2. Run the application:

```bash
python app.py
```

3. Open a browser and navigate to `http://127.0.0.1:5000`

## Simplified Run Script

You can also use the provided run script which checks dependencies and runs the application:

```bash
python run_app.py
```

## Deployment Options

### Deploy to Heroku

1. Create a Heroku account at https://signup.heroku.com/

2. Install the Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

3. Login to Heroku:

```bash
heroku login
```

4. Create a new Heroku app:

```bash
heroku create birthday-crypto-app
```

5. Deploy to Heroku:

```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

6. Open the app:

```bash
heroku open
```

### Deploy to Render

1. Create a Render account at https://render.com/

2. Create a new Web Service

3. Link your GitHub repository or upload the code directly

4. Configure the service:
   - Build Command: `pip install -r requirements_web.txt`
   - Start Command: `gunicorn app:app`

5. Click "Create Web Service"

### Deploy to PythonAnywhere

1. Create a PythonAnywhere account at https://www.pythonanywhere.com/

2. Upload your files using the Files tab or via GitHub

3. Create a new web app:
   - Select "Flask" as the framework
   - Choose Python 3.8 or higher
   - Set the path to your app.py file

4. Install required packages:

```bash
pip install -r requirements_web.txt
```

5. Configure the WSGI file to point to your Flask app

## Customizing the Birthday Challenge

The birthday challenge is personalized for Lisa's birthday (April 4th). The challenges include:

1. The Caesar cipher message with a shift key of 4 (Lisa's birth date)
2. The Vigenère cipher message with the key "april" (Lisa's birth month)
3. A final Base64 encoded personal message

## Important Note

When deploying to free hosting services, there might be limitations with file storage. The steganography feature requires writing files to the server. Some platforms like Heroku have ephemeral file systems, meaning files are deleted when the app is restarted.

For the best experience with the steganography feature, consider using a hosting service that provides persistent file storage. 