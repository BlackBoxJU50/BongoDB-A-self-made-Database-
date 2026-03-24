# BongoDB Portable (v2.0)

**BongoDB** is the "Self-Made" Database solution for developers who want to skip the cost of a traditional database. It turns your **Google Sheets** into a metadata engine and your **Google Drive** into a file storage system.

## 🚀 Getting Started

If you just cloned this project, follow these steps to set up your own BongoDB:

### 1. Install Dependencies
Run this in your terminal:
```bash
pip install -r requirements.txt
```

### 2. Google Cloud Setup (One-time)
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  **Enable APIs**: Search for and **Enable** both the **Google Drive API** and **Google Sheets API**.
3.  **OAuth Consent Screen**:
    *   Set User Type to **External**.
    *   Add your own email under **Test Users** (Critical!).
    *   Add scopes: `.../auth/drive` and `.../auth/spreadsheets`.
4.  **Credentials**: 
    *   Go to **Create Credentials** > **OAuth client ID**.
    *   Select **Desktop app**.
    *   Download the JSON file, rename it to **`client_secrets.json`**, and put it in this project folder.

### 3. Create your "Database"
1.  **Metadata**: Create a new [Google Sheet](https://sheet.new). Copy the ID from the URL (between `/d/` and `/edit`).
2.  **Storage**: Create a new [Google Drive Folder](https://drive.google.com). Copy the ID from the end of the URL.
3.  **Config**: Open `config.py` and paste your IDs:
    ```python
    SPREADSHEET_ID = 'your_id_here'
    DRIVE_ROOT_FOLDER_ID = 'your_id_here'
    ```

### 4. Run BongoDB
```bash
python3 main.py
```
A browser will open for a one-time login. Once authorized, you are ready to use your free, self-hosted database!

---

## 🛠 Features
- **Zero Cost**: Built for developers using free Google storage.
- **Simplified UID**: Auto-generates human-readable IDs (`Name-12345678`).
- **Secure**: Passwords are saved as secure hashes (`pbkdf2:sha256`).
- **Portable**: Just carry your code and `client_secrets.json`.

---
*Created with ❤️ for the Developer Community.*
