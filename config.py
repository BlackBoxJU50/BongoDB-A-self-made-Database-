import os

# Google API IDs (To be filled by the user or set via environment variables)
SPREADSHEET_ID = os.getenv('BONGODB_SHEET_ID', 'YOUR_SPREADSHEET_ID_HERE')
DRIVE_ROOT_FOLDER_ID = os.getenv('BONGODB_DRIVE_FOLDER_ID', 'YOUR_DRIVE_FOLDER_ID_HERE')

# Security
SECRET_KEY = os.getenv('BONGODB_SECRET_KEY', 'SUPER_SECRET_KEY_FOR_FLASK')

# Sheets Metadata Schema (Master Specification Alignment)
# UID | Name | Email | Password | Folder_ID | Image_URL
HEADERS = ['UID', 'Name', 'Email', 'Password', 'Folder_ID', 'Image_URL']
USERS_SHEET_NAME = 'Users'
