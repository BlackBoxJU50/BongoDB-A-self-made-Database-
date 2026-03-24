import os
from werkzeug.security import generate_password_hash
from datetime import datetime

class MockBongoDB:
    def __init__(self, credentials_path):
        self.users = []
        # Add a default test user matching the new schema
        # UID | Name | Email | Password | Folder_ID | Image_URL
        self.users.append({
            'UID': 'test-uid-123',
            'Name': 'Test User',
            'Email': 'test@example.com',
            'Password': generate_password_hash('testpass'),
            'Folder_ID': 'mock_folder_123',
            'Image_URL': 'https://drive.google.com/thumbnail?id=mock_image_123'
        })

    def get_sheet(self):
        return self

    def add_user(self, uid, name, email, hashed_password, folder_id, image_url):
        self.users.append({
            'UID': uid,
            'Name': name,
            'Email': email,
            'Password': hashed_password,
            'Folder_ID': folder_id,
            'Image_URL': image_url
        })

    def get_user_by_uid(self, uid):
        for user in self.users:
            if str(user['UID']) == str(uid):
                return user
        return None

class MockDriveIO:
    def __init__(self, credentials_path):
        pass

    def create_uid_folder(self, uid):
        return f"mock_folder_{uid}"

    def upload_image(self, file_path, folder_id):
        file_id = f"mock_file_{os.path.basename(file_path)}"
        image_url = f"https://drive.google.com/thumbnail?id={file_id}"
        return file_id, image_url

    def get_file_content(self, file_id):
        return b"Mock file content for " + file_id.encode()

# Monkeypatching the real modules for testing
from modules import bongo_db, drive_io

bongo_db.BongoDB = MockBongoDB
drive_io.DriveIO = MockDriveIO

print("Mock handlers updated for Master Specification.")
