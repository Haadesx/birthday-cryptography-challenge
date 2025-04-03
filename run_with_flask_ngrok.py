from flask import Flask
from flask_ngrok import run_with_ngrok
from app import app as flask_app

# Monkey-patch the route handlers from app.py
for rule in flask_app.url_map.iter_rules():
    view_func = flask_app.view_functions[rule.endpoint]
    app = Flask(__name__)
    app.add_url_rule(rule.rule, view_func=view_func, methods=rule.methods)

# Enable ngrok
run_with_ngrok(app)

if __name__ == '__main__':
    print("Starting Flask app with ngrok...")
    print("A public URL will be generated automatically.")
    print("Wait for 'Running on...' message which will show your public URL.")
    app.run() 