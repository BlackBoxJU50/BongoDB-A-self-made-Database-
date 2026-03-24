from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from flask_cors import CORS
import json
import os
import sys
import time
from werkzeug.utils import secure_filename

# Add root to path for modules import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from modules.auth_manager import AuthManager

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
CORS(app)

SETTINGS_FILE = 'settings.json'

def get_settings():
    base_dir = AuthManager.get_base_dir()
    settings_path = os.path.join(base_dir, SETTINGS_FILE)
    
    # Default from config
    settings = {
        'spreadsheet_id': config.SPREADSHEET_ID,
        'drive_id': config.DRIVE_ROOT_FOLDER_ID
    }
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                saved = json.load(f)
                settings.update(saved)
        except:
            pass
    return settings

def sanitize_id(id_string):
    if not id_string: return ""
    # Extract ID from Google URL if present
    # e.g. https://docs.google.com/spreadsheets/d/1ABC123/edit -> 1ABC123
    if "/d/" in id_string:
        parts = id_string.split("/d/")
        if len(parts) > 1:
            return parts[1].split("/")[0]
    return id_string.strip()

def save_settings(ss_id, dr_id):
    ss_id = sanitize_id(ss_id)
    dr_id = sanitize_id(dr_id)
    base_dir = AuthManager.get_base_dir()
    settings_path = os.path.join(base_dir, SETTINGS_FILE)
    print(f"[*] Saving settings to: {settings_path}")
    with open(settings_path, 'w') as f:
        json.dump({'spreadsheet_id': ss_id, 'drive_id': dr_id}, f)

def get_db():
    base_dir = AuthManager.get_base_dir()
    creds_path = os.path.join(base_dir, config.CLIENT_SECRETS_FILE)
    
    if not os.path.exists(creds_path):
        return "MISSING_CREDS"

    try:
        creds = AuthManager.get_credentials()
        if not creds:
            print("[!] get_db: No credentials returned from AuthManager.")
            return None
        
        # Load dynamic settings
        settings = get_settings()
        
        # Override config IDs for this instance (for other modules)
        config.SPREADSHEET_ID = settings['spreadsheet_id']
        config.DRIVE_ROOT_FOLDER_ID = settings['drive_id']
        
        auth_mgr = AuthManager(creds, spreadsheet_id=settings['spreadsheet_id'])
        if not auth_mgr.db:
            print("[!] get_db: AuthManager initialized but database engine is None.")
            return None
            
        return auth_mgr.db
    except Exception as e:
        print(f"[!] CRITICAL DB INIT ERROR: {e}")
        import traceback
        traceback.print_exc()
        return str(e) # Return the error string to show in UI

@app.route('/authenticate')
def authenticate():
    try:
        creds = AuthManager.get_credentials()
        if creds:
            return redirect(url_for('dashboard'))
        else:
            return render_template('error.html', title="Invalid Credentials", msg="Auth failed.")
    except Exception as e:
        return f"Auth Error: {e}", 500

@app.route('/')
def dashboard():
    db = get_db()
    
    if db == "MISSING_CREDS":
        settings = get_settings()
        return render_template('setup.html', curr_ss=settings['spreadsheet_id'], curr_dr=settings['drive_id'])
    
    if not db or isinstance(db, str):
        # Pass the error string if db initialization failed
        error_str = db if isinstance(db, str) else "Could not connect to Google Cloud."
        
        # If it's a permission error, it's likely they need to set their own IDs
        if "permission" in error_str.lower() or "403" in error_str:
            settings = get_settings()
            return render_template('setup.html', 
                                   curr_ss=settings['spreadsheet_id'], 
                                   curr_dr=settings['drive_id'],
                                   error="Permission Denied: BongoDB can't access that Database ID. Please enter your OWN Database ID and Asset ID below.")

        # AGGRESSIVE TERMINAL LOGGING for the developer
        if "disabled" in error_str.lower():
            print("\n" + "!"*60)
            print("🛑 CRITICAL: GOOGLE SHEETS API IS DISABLED")
            print("👉 ENABLE IT HERE: https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=225750268761")
            print("!"*60 + "\n")
            
        return render_template('auth_required.html', 
                               title="Connection Status",
                               msg=error_str,
                               error=error_str)
    
    # List all worksheets (Collections)
    try:
        sheets = db.spreadsheet.worksheets()
        collections = []
        for s in sheets:
            collections.append({
                'name': s.title,
                'rows': s.row_count,
                'cols': s.col_count
            })
    except Exception as e:
        return render_template('error.html', title="Connection Error", msg=f"Could not reach Google Sheets: {e}")
        
    settings = get_settings()
    return render_template('dashboard.html', collections=collections, spreadsheet_id=settings['spreadsheet_id'])

@app.route('/setup', methods=['GET', 'POST'])
def setup_wizard():
    settings = get_settings()
    
    if request.method == 'POST':
        ss_id = request.form.get('spreadsheet_id')
        dr_id = request.form.get('drive_id')
        save_settings(ss_id, dr_id)
        
        # In a binary, we don't reload config.py, we just use the new settings in next get_db()
        return redirect(url_for('authenticate'))
        
    return render_template('setup.html', curr_ss=settings['spreadsheet_id'], curr_dr=settings['drive_id'])

@app.route('/collection/<name>')
def view_collection(name):
    db = get_db()
    col = db.collection(name, [])
    data = col.find_all()
    headers = data[0].keys() if data else []
    return render_template('collection.html', name=name, data=data, headers=headers)

# --- PROFESSIONAL REST API ---
@app.route('/api/v1/insert', methods=['POST'])
def api_insert():
    db = get_db()
    req = request.json
    col_name = req.get('collection')
    data = req.get('data') # Expecting list or dict
    
    col = db.collection(col_name, list(data.keys()) if isinstance(data, dict) else [])
    if isinstance(data, dict):
        col.insert(list(data.values()))
    else:
        col.insert(data)
    return jsonify({"status": "success", "message": "Data written to cloud"}), 201

@app.route('/api/v1/find', methods=['GET'])
def api_find():
    db = get_db()
    col_name = request.args.get('collection')
    col = db.collection(col_name, [])
    return jsonify(col.find_all())

@app.route('/api/v1/create_collection', methods=['POST'])
def api_create_collection():
    db = get_db()
    
    if not db or isinstance(db, str):
        return jsonify({"status": "error", "error": "Database connection failed. Please check your credentials and Spreadsheet ID."}), 500
        
    req = request.json
    col_name = req.get('name')
    headers = req.get('headers')

    
    if not col_name or not headers:
        return jsonify({"status": "error", "error": "Missing name or headers"}), 400
        
    try:
        # Initializing the collection will automatically create it in the sheet if it doesn't exist
        db.collection(col_name, headers)
        return jsonify({"status": "success", "message": "Collection created successfully"}), 201
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/docs')
def docs():
    return render_template('docs.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
