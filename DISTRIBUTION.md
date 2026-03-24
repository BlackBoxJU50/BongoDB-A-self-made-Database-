# Distribution & Integration Guide 📦

To let another developer use BongoDB as a professional product without seeing your source code, follow these steps:

## 1. Compile into a Single Binary
Use **PyInstaller** to turn the Python code into a standalone `.exe` or `.app`.
```bash
# Install PyInstaller
pip install pyinstaller

# Build the project (use -m if pyinstaller command is not found)
python3 -m PyInstaller --onefile --noconsole --add-data "web:web" --name BongoDB main.py
```
This generates a single `BongoDB` file in the `dist/` folder. **This is the file you give to other developers.** They won't see your code.

## 2. How the Other Developer Uses It
1.  **Download**: The developer downloads your compiled `BongoDB` software.
2.  **Secrets**: They place their own Google `client_secrets.json` in the same folder as the software.
3.  **Run**: They double-click the software.
4.  **Setup**: The BongoDB Browser opens. They paste their own `SPREADSHEET_ID` and `DRIVE_ROOT_FOLDER_ID`.
5.  **Integration**: They can now write code in **THEIR OWN** project (Node.js, React, etc.) and save data to **THEIR OWN** cloud via `http://localhost:5001/api/v1/insert`.

## 3. Integration Examples

### Node.js / React
```javascript
const BongoDB = {
  insert: async (col, data) => {
    return await fetch('http://localhost:5001/api/v1/insert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ collection: col, data: data })
    });
  }
};

// Usage:
BongoDB.insert('Sales', { product: 'Coffee', amount: 5 });
```

### Python
```python
import requests
requests.post('http://localhost:5001/api/v1/insert', json={
    'collection': 'Logs',
    'data': {'event': 'Server Started', 'user': 'Admin'}
})
```

---
BongoDB makes Google Sheets act like a **Real Database Server** for any language.
