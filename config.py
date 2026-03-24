import os

# Google API IDs (To be filled by the user or set via environment variables)
SPREADSHEET_ID = '1MW5xXVFdO4l8TEsJuMZ51O7qIFQ--hc790RJo_ofozU'
DRIVE_ROOT_FOLDER_ID = '1PGMu8fQuqsFnKcu5783tl-FMUAjfJUrL'

# OAuth 2.0 Files
CLIENT_SECRETS_FILE = 'client_secrets.json'
TOKEN_FILE = 'token.json'

# Security
SECRET_KEY = os.getenv('BONGODB_SECRET_KEY', 'SUPER_SECRET_KEY_FOR_FLASK')

# Cloud Collection Metadata (Optional defaults)
# The developer can define any headers when creating a collection via BongoDB(creds).collection(name, headers)
HEADERS = ['ID', 'Timestamp', 'Data'] 
