from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
from modules.bongo_db import BongoDB
from modules.drive_io import DriveIO

class AuthManager:
    def __init__(self, credentials_path):
        self.db = BongoDB(credentials_path)
        self.drive = DriveIO(credentials_path)

    def register(self, name, email, password, image_path):
        # 1. Generate unique UID (UUID4)
        uid = str(uuid.uuid4())

        # 2. Drive Logic: Create folder named UID and upload image
        try:
            folder_id = self.drive.create_uid_folder(uid)
            file_id, image_url = self.drive.upload_image(image_path, folder_id)
        except Exception as e:
            return False, f"Drive Error: {str(e)}"

        # 3. Sheet Logic: Append row
        hashed_password = generate_password_hash(password)
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
