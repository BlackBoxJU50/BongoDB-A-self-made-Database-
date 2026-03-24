import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from modules.bongo_db import BongoDB
from modules.drive_io import DriveIO
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import json
from config import CLIENT_SECRETS_FILE, TOKEN_FILE

# OAuth Scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class AuthManager:
    def __init__(self, credentials=None):
        self.creds = credentials
        if credentials:
            self.db = BongoDB(credentials)
            self.drive = DriveIO(credentials)

    @staticmethod
    def get_credentials():
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CLIENT_SECRETS_FILE):
                    raise FileNotFoundError(f"{CLIENT_SECRETS_FILE} not found. Please download it from Google Cloud Console.")
                
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        return creds

    def self_check(self):
        # 1. Check Sheet Access
        try:
            self.db.get_sheet()
        except Exception as e:
            return False, f"Google Sheet Access Error: {e}\nTIP: Make sure you shared the sheet with the service account email as Editor."
            
        # 2. Check Drive Access
        try:
            self.drive.service.files().get(fileId=self.drive.credentials_path if hasattr(self.drive, 'credentials_path') else os.getenv('BONGODB_DRIVE_FOLDER_ID')).execute()
        except:
            # Fallback check: list files in root folder
            from config import DRIVE_ROOT_FOLDER_ID
            try:
                self.drive.service.files().get(fileId=DRIVE_ROOT_FOLDER_ID).execute()
            except Exception as e:
                return False, f"Google Drive Access Error: {e}\nTIP: Make sure you shared the folder with the service account email as Editor."
                
        return True, "All systems operational!"

    def register(self, name, email, password, image_path):
        # 1. Generate unique UID (UUID4)
        uid = str(uuid.uuid4())

        # 2. Drive Logic: Create folder named UID and upload image
        try:
            folder_id = self.drive.create_uid_folder(uid)
            file_id, image_url = self.drive.upload_image(image_path, folder_id)
        except Exception as e:
            return False, f"Drive Error: {str(e)}"

        # 2. Hash password (using pbkdf2:sha256 as fallback for scrypt issues)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            self.db.add_user(uid, name, email, hashed_password, folder_id, image_url)
        except Exception as e:
            return False, f"Sheet Error: {str(e)}"

        return True, uid

    def login(self, uid, password):
        user = self.db.get_user_by_uid(uid)
        if user and check_password_hash(user['Password'], password):
            return True, user
        return False, "Invalid UID or Password"
