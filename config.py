import os

# Google API IDs (To be filled by the user or set via environment variables)
SPREADSHEET_ID = os.getenv('BONGODB_SHEET_ID', '1e92yDXleN0ybKSvLbqVhvK89CzySRbCfzrDWCsFOAnY')
DRIVE_ROOT_FOLDER_ID = os.getenv('BONGODB_DRIVE_FOLDER_ID', '1Bi0nn6ub6hpkvh3lEP-GOUgIG7ApTXgf')

# OAuth 2.0 Files
CLIENT_SECRETS_FILE = 'client_secrets.json'
TOKEN_FILE = 'token.json'

# Security
SECRET_KEY = os.getenv('BONGODB_SECRET_KEY', 'SUPER_SECRET_KEY_FOR_FLASK')

# Sheets Metadata Schema (Master Specification Alignment)
# UID | Name | Email | Password | Folder_ID | Image_URL
HEADERS = ['UID', 'Name', 'Email', 'Password', 'Folder_ID', 'Image_URL']
USERS_SHEET_NAME = 'Users'
