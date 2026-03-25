from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "SAMPLE_WEBSITE_SECRET_KEY"

# BongoDB API Base (BongoDB must be running on port 5001)
BONGODB_URL = "http://localhost:5001/api/v1"

# Local upload folder for the demo website
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        image = request.files.get('image')
        
        if not image or image.filename == '':
            flash("Please upload a profile image", "error")
            return redirect(url_for('signup'))

        # 1. Upload Image to BongoDB Drive
        files = {'file': (image.filename, image.stream, image.mimetype)}
        try:
            upload_res = requests.post(f"{BONGODB_URL}/upload", files=files)
            if upload_res.status_code != 201:
                flash(f"Image Upload Failed: {upload_res.json().get('error')}", "error")
                return redirect(url_for('signup'))
            
            image_url = upload_res.json().get('url')
            
            # 2. Insert User Data to BongoDB
            user_data = {
                "collection": "Users",
                "data": {
                    "Name": name,
                    "Email": email,
                    "Password": password,
                    "ImageURL": image_url
                }
            }
            insert_res = requests.post(f"{BONGODB_URL}/insert", json=user_data)
            if insert_res.status_code == 201:
                flash("Signup Successful! Please Login.", "success")
                return redirect(url_for('login'))
            else:
                flash(f"Signup Failed: {insert_res.json().get('error')}", "error")
        except Exception as e:
            flash(f"Connection to BongoDB failed: {e}", "error")
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Fetch users from BongoDB using existing /api/v1/find
        try:
            res = requests.get(f"{BONGODB_URL}/find?collection=Users")
            if res.status_code == 200:
                users = res.json()
                # Stringify both to avoid integer/string mismatch
                user = next((u for u in users if str(u.get('Email')) == str(email) and str(u.get('Password')) == str(password)), None)
                if user:
                    session['user'] = user
                    return redirect(url_for('profile'))
                else:
                    flash("Invalid credentials", "error")
            else:
                flash("Database error or collection not found", "error")
        except Exception as e:
            flash(f"Connection to BongoDB failed: {e}", "error")
            
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Running on port 5002 to avoid conflict with BongoDB
    app.run(port=5002, debug=True)
