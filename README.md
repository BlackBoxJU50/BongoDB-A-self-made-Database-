# 🦍 BongoDB Portable (v2.0)
**The Ultimate Self-Made Cloud Database Engine**

BongoDB is a professional developer tool that transforms your **Google Sheets** into a high-performance NoSQL Cloud Database, and your **Google Drive** into a robust file storage backend. It allows you to build E-commerce platforms, Blogs, and Web Apps effortlessly without paying for traditional database hosting.

---

## 🌟 Why Choose BongoDB?
- **Zero Cost Cloud**: Your data is hosted on Google's global infrastructure for free forever.
- **No Local Storage**: BongoDB acts purely as an API gateway to the cloud.
- **Professional Dashboard**: Manage collections, browse data, and monitor performance through a premium glassmorphic web interface.
- **Developer API**: Seamlessly integrate with React, Node.js, PHP, or Python using our straightforward RESTful API.

---

## 🚀 Installation & Setup

Follow these steps to set up BongoDB on your local machine or server.

### Prerequisites
- Python 3.9+ installed and added to PATH.
- `uv` package manager (optional but recommended for speed) or standard `pip`.

### Step 1: Clone and Install
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/BlackBoxJU50/BongoDB-A-self-made-Database-.git
cd BongoDB-A-self-made-Database-

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies using pip
pip install -r requirements.txt
```

### Step 2: Configure Google Cloud OAuth
BongoDB uses the **Google OAuth 2.0 Installed App Flow** to ensure maximum security.
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new Project (or select an existing one).
3. Enable the **Google Sheets API** and the **Google Drive API**.
4. Go to **APIs & Services > OAuth consent screen**. Create an "**External**" app and add yourself as a **Test User**.
5. Go to **Credentials**, click **Create Credentials** -> **OAuth client ID**. Choose "**Desktop app**".
6. Download the generated JSON file and rename it to `client_secrets.json`.
7. Place `client_secrets.json` directly into your main BongoDB directory (or the `dist/` directory if using the compiled binary).

### Step 3: Start the Engine
Run the main server script:
```bash
python3 main.py
```
*(If you are using the compiled binary, simply double-click the `BongoDB` executable inside the `dist/` folder).*

---

## 📖 User Guide

### 1. Activating the Cloud Engine
Upon running the BongoDB server for the first time, your browser will prompt you to log into your Google Account. 
- Log in with the Google Account that will act as the "Admin" of the database.
- BongoDB will open a web interface on `http://localhost:5001`.

### 2. Linking Your Database (Setup Wizard)
You will be greeted by the Setup Wizard. You need to provide:
1. **DATABASE ID (Google Sheets)**: 
   - Create a blank Google Spreadsheet.
   - Look at the URL: `https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit`. Copy `YOUR_SPREADSHEET_ID`.
   - **Crucial Permission Step**: Ensure the Google Account you logged into BongoDB with has **Editor** access to this spreadsheet!
2. **ASSET STORAGE ID (Google Drive)**:
   - Create a folder in Google Drive. Copy the ID from the URL exactly like above.

### 3. Managing Collections (Dashboard)
Once connected, you will see the **Developer Dashboard**.
- **+ New Collection**: Click this button to create a new Table (Worksheet). Provide the name and comma-separated column headers (e.g., `id, title, price`). BongoDB automatically initializes the headers in your Cloud Sheet.
- **Browse Data**: Click on any collection to view the records in a beautiful data grid.

---

## 🔗 Developer Integration

BongoDB exposes a clean **RESTful API** on port `5001`. You use this API in your frontend or backend applications exactly like how you would communicate with a real hosted database limitlessly.

### 1. Insert Data (POST)
**Endpoint**: `/api/v1/insert`

#### Example (Node.js / React)
```javascript
const response = await fetch('http://localhost:5001/api/v1/insert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    collection: 'Products',
    data: { 
      "Name": "MacBook Pro", 
      "Price": "1999" 
    }
  })
});
```

### 2. Retrieve Data (GET)
**Endpoint**: `/api/v1/find?collection=COLLECTION_NAME`

#### Example (Python)
```python
import requests

response = requests.get('http://localhost:5001/api/v1/find?collection=Products')
print(response.json())
# Output: [{ "Name": "MacBook Pro", "Price": "1999" }]
```

---

## 📦 Compiling to Standalone Binary

You can distribute BongoDB as a single `.exe` or `.app` to other developers, hiding your source code entirely! 
1. Install PyInstaller: `pip install pyinstaller`
2. Build the binary from the root directory:
```bash
python3 -m PyInstaller --onefile --noconsole --add-data "web:web" --name BongoDB main.py
```
The final standalone database binary will be available in the `dist/` directory.

---
**Built by Developers, for Developers. BongoDB is part of the BlackBox Open Source Initiative.**
