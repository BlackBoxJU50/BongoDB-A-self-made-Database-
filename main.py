import argparse
import sys
import json
import os
from modules.auth_manager import AuthManager

def main():
    print("Welcome to BongoDB Portable (v2.0) - OAuth Edition")
    
    # Trigger OAuth flow
    try:
        creds = AuthManager.get_credentials()
        auth = AuthManager(creds)
    except Exception as e:
        print(f"\n[!] Authentication Failed: {e}")
        print(f"Make sure 'client_secrets.json' is in the project root.")
        sys.exit(1)
    
    print("Performing system self-check...")
    ok, status = auth.self_check()
    if not ok:
        print(f"\n[!] SYSTEM CHECK FAILED:\n{status}")
        # We don't exit, but warn the user.
    else:
        print(f"[*] {status}")

    while True:
        print("\n--- BongoDB CLI ---")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            image_path = input("Image Path (Local path to an image): ")
            
            if not os.path.exists(image_path):
                print("Image file not found!")
                continue

            success, uid = auth.register(name, email, password, image_path)
            if success:
                print(f"Registration Successful! Your Unique ID is: {uid}")
            else:
                print(f"Registration Failed: {uid}")

        elif choice == '2':
            uid = input("UID: ")
            password = input("Password: ")
            
            success, result = auth.login(uid, password)
            if success:
                print(f"Login Successful! Fetching user info...")
                # Fetching user info and launching web view
                # In a real scenario, we might want to pass the session to Flask
                # For this task, we can just save it to a temporary file for the server to read
                with open('.web_session.json', 'w') as f:
                    json.dump(result, f)
                
                print("Launching Profile Viewer at http://127.0.0.1:5001")
                print("Press Ctrl+C to stop the server and return to CLI.")
                try:
                    import subprocess
                    subprocess.run([sys.executable, 'web/server.py'])
                except KeyboardInterrupt:
                    print("\nReturning to CLI...")
            else:
                print(result)

        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
