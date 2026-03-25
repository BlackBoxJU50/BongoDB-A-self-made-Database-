import os
import sys
import random
from modules.bongo_db import BongoDB
from modules.drive_io import DriveIO
import google_auth_oauthlib.flow
import google.auth.transport.requests
import google.oauth2.credentials
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from config import CLIENT_SECRETS_FILE, TOKEN_FILE, HEADERS

# OAuth Scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class AuthManager:
    def __init__(self, credentials=None, spreadsheet_id=None):
        if credentials:
            self.db = BongoDB(credentials, spreadsheet_id)
            self.drive = DriveIO(credentials)
        else:
            self.db = None
            self.drive = None

    @staticmethod
    def get_base_dir():
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    @staticmethod
    def get_credentials():
        base_dir = AuthManager.get_base_dir()
        token_path = os.path.join(base_dir, TOKEN_FILE)
        secrets_path = os.path.join(base_dir, CLIENT_SECRETS_FILE)
        
        print(f"[*] BongoDB Path Debug: {base_dir}")
        
        creds = None
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception as e:
                print(f"[!] Error loading token: {e}")
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"[!] Token Refresh Failed: {e}")
                    creds = None
            
            if not creds or not creds.valid:
                if not os.path.exists(secrets_path):
                    print(f"[!] Secrets Missing at: {secrets_path}")
                    return None
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        secrets_path, SCOPES)
                    # Force prompt='consent' to ensure user sees all requested scopes (Drive + Sheets)
                    creds = flow.run_local_server(port=0, 
                                                authorization_prompt_message='BongoDB Cloud Engine: Requesting Permissions...',
                                                prompt='consent')
                except Exception as e:
                    print(f"[!] OAuth Flow Error: {e}")
                    import traceback
                    traceback.print_exc()
                    return None
            
            if creds:
                # Save the credentials for the next run
                try:
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())
                    print(f"[*] Credentials saved successfully to: {token_path}")
                except Exception as e:
                    print(f"[!] Failed to save token.json: {e}")
        
        return creds

    def self_check(self, spreadsheet_id, drive_id):
        # 1. Check Sheet Access
        try:
            if not spreadsheet_id: return False, "SPREADSHEET_ID not set"
            self.db.client.open_by_key(spreadsheet_id)
        except Exception as e:
            return False, f"Google Sheet Access Error: {e}"
            
        # 2. Check Drive Access
        try:
            if not drive_id: return False, "DRIVE_ROOT_FOLDER_ID not set"
            self.drive.service.files().get(fileId=drive_id).execute()
        except Exception as e:
            return False, f"Google Drive Access Error: {e}"
                 
        return True, "Cloud Storage Connected!"

    @staticmethod
    def disconnect():
        base_dir = AuthManager.get_base_dir()
        token_path = os.path.join(base_dir, TOKEN_FILE)
        if os.path.exists(token_path):
            os.remove(token_path)
            return True
        return False
