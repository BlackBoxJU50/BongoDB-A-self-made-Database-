import sys
import os
import webbrowser
import threading
import time

# Add root to path for modules import
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from web.server import app

def open_browser():
    """Wait for server to start then open browser."""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5001")

def main():
    print("--- BongoDB Professional v2.0 ---")
    print("[*] Initializing Web Dashboard...")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask Server
    print("[*] BongoDB Engine is running at http://127.0.0.1:5001")
    print("[!] Press Ctrl+C to shutdown.")
    app.run(port=5001, debug=False)

if __name__ == "__main__":
    main()
