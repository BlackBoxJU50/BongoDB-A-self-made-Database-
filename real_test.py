import os
import sys
import subprocess
import time

def run_real_test():
    print("--- Testing Real Registration ---")
    # Initial Handshake (should find credentials.json)
    # Choice 1: Signup
    # Name: Test User
    # Email: testuser@example.com
    # Password: testpassword
    # Image Path: README.md
    # Choice 3: Exit
    
    reg_inputs = "1\nTest User\ntestuser@example.com\ntestpassword\nREADME.md\n3\n"
    result = subprocess.run(
        [sys.executable, 'main.py'],
        input=reg_inputs,
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
    
    uid = None
    for line in result.stdout.split('\n'):
        if "Your Unique ID is:" in line:
            uid = line.split("Your Unique ID is:")[1].strip()
            break
            
    if uid:
        print(f"\nREAL VERIFICATION SUCCESSFUL! UID CREATED: {uid}")
        print("You can now log in with this UID.")
    else:
        print("\nREAL VERIFICATION FAILED. Check the output above for errors.")

if __name__ == "__main__":
    run_real_test()
