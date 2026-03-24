from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import sys
import os

# Add root to path for config import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DRIVE_ROOT_FOLDER_ID

class DriveIO:
    def __init__(self, credentials_path):
        scopes = ['https://www.googleapis.com/auth/drive']
        self.credentials = Credentials.from_service_account_file(
            credentials_path, scopes=scopes
        )
        self.service = build('drive', 'v3', credentials=self.credentials)

    def create_uid_folder(self, uid):
        # Task 1: Create a folder named after the UID
        file_metadata = {
            'name': str(uid),
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [DRIVE_ROOT_FOLDER_ID]
        }
        file = self.service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

    def upload_image(self, file_path, folder_id):
        # Task 1: Upload the file inside that folder
        filename = os.path.basename(file_path)
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        file_id = file.get('id')

        # Task 1: Update the folder permissions so the link is viewable by the user
        self.service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        # Task 3: Converting the file_id into a "thumbnail/export" link
        image_url = f"https://drive.google.com/thumbnail?id={file_id}"
        return file_id, image_url

    def get_file_content(self, file_id):
        return self.service.files().get_media(fileId=file_id).execute()
