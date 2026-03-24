from flask import Flask, render_template, request, session, redirect, url_for
import json
import os
import sys

# Add root to path for config and modules import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    if os.path.exists('.web_session.json'):
        with open('.web_session.json', 'r') as f:
            user_data = json.load(f)
        return render_template('profile.html', user=user_data)
    return "No active session. Please log in via CLI.", 401

if __name__ == "__main__":
    app.run(debug=True, port=5001)
