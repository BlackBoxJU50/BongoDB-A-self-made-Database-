import os
import sys
import subprocess
import time

def run_cli_session():
    # Since main.py uses interactive inputs, we'll use a script to pipe inputs to it.
    inputs = [
        "mock_credentials.json", # Initial Handshake
        "1",                    # Signup
        "John Doe",             # Name
        "john@example.com",     # Email
        "securepass",           # Password
        "README.md",            # Image Path
        "2",                    # Login
        "last_uid",             # UID (placeholder)
        "securepass",           # Password
        "3"                     # Exit
    ]
    
    # We need to capture the UID from the output of the signup command to use it in login.
    # This is tricky with subprocess.run. We'll do a simpler approach: 
    # run registration once, then login with the generated UID.
    
    print("--- Testing Registration ---")
    reg_inputs = "mock_credentials.json\n1\nJohn Doe\njohn@example.com\nsecurepass\nREADME.md\n3\n"
    result = subprocess.run(
        [sys.executable, 'main.py'],
        input=reg_inputs,
        capture_output=True,
        text=True,
        env={**os.environ, "BONGODB_MOCK": "1"}
    )
    
    print(result.stdout)
    
    uid = None
    for line in result.stdout.split('\n'):
        if "Your Unique ID is:" in line:
            uid = line.split("Your Unique ID is:")[1].strip()
            break
    
    if uid:
        print(f"Captured UID: {uid}")
        print("\n--- Testing Login ---")
        login_inputs = f"mock_credentials.json\n2\n{uid}\nsecurepass\n3\n"
        # We won't actually launch the web server in the test to avoid blocking
        # But we can check if it tries to launch it.
        result = subprocess.run(
            [sys.executable, 'main.py'],
            input=login_inputs,
            capture_output=True,
            text=True,
            env={**os.environ, "BONGODB_MOCK": "1"}
        )
        print(result.stdout)
    else:
        print("Failed to capture UID from registration.")

def main():
    # Create a dummy credentials file for the handshake
    with open('mock_credentials.json', 'w') as f:
        f.write('{"type": "service_account"}')
        
    print("Starting BongoDB Portable Verification Suite\n")
    run_cli_session()
    
    # Clean up
    if os.path.exists('mock_credentials.json'):
        os.remove('mock_credentials.json')

if __name__ == "__main__":
    main()
