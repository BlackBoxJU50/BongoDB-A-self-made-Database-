# BongoDB Portable v2.0

BongoDB Portable is a CLI-driven database gateway using Google Sheets for metadata and Google Drive for file storage.

## Features
- CLI-based user registration and login.
- Secure metadata storage in Google Sheets.
- File storage in Google Drive with user-specific isolation.
- Flask-based web view for user profiles and image galleries.

## Prerequisites
- Python 3.x
- Google Service Account `credentials.json`
- Google Sheet ID and Google Drive Folder ID

## Setup
1.  Install dependencies: `pip install -r requirements.txt`
2.  Configure `config.py` with your IDs and service account file path.
3.  Run the CLI: `python main.py --help`
4.  Run the Web View: `python app.py`
