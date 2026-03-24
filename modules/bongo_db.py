import gspread
from google.oauth2.service_account import Credentials
import sys
import os

# Add root to path for config import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import SPREADSHEET_ID, USERS_SHEET_NAME, HEADERS

class BongoDB:
    def __init__(self, credentials):
        # Initialize gspread with the provided OAuth credentials
        self.client = gspread.authorize(credentials)
        self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
        self.sheet = self.get_sheet()

    def get_sheet(self):
        try:
            return self.spreadsheet.worksheet(USERS_SHEET_NAME)
        except gspread.exceptions.WorksheetNotFound:
            # Task 2: The Spreadsheet Auto-Setup
            sheet = self.spreadsheet.add_worksheet(title=USERS_SHEET_NAME, rows=100, cols=len(HEADERS))
            sheet.update('A1:F1', [HEADERS])
            return sheet

    def add_user(self, uid, name, email, hashed_password, folder_id, image_url):
        sheet = self.get_sheet()
        sheet.append_row([uid, name, email, hashed_password, folder_id, image_url])

    def get_user_by_uid(self, uid):
        sheet = self.get_sheet()
        users = sheet.get_all_records()
        for user in users:
            if str(user['UID']) == str(uid):
                return user
        return None
