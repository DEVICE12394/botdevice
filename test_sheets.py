import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Config ---
CREDENTIALS_FILE = "snappy-topic-481406-p9-3673e43ccb98.json"
SPREADSHEET_ID = "1qQgazyaUQfNcoLNAxU5a2x9utAQl8zNE5FYMUPxdyQU"

def test_google_sheets():
    print("="*50)
    print("TESTING GOOGLE SHEETS CONNECTION")
    print("="*50)

    # 1. Check File
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"[ERROR] Cannot find file {CREDENTIALS_FILE}")
        return

    print(f"[OK] Credentials file found: {CREDENTIALS_FILE}")

    try:
        # 2. Authenticate
        print("[INFO] Authenticating...")
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        print("[OK] Authentication successful")

        # 3. Open Sheet
        print(f"[INFO] Opening sheet ID: {SPREADSHEET_ID}...")
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        print(f"[OK] Sheet opened: '{sheet.title}'")

        # 4. Write Test Row
        print("[INFO] Attempting to write test row...")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_row = [timestamp, "TEST_USER", "Test Script", "System Check", "Connection Successful"]
        
        sheet.append_row(test_row)
        print("[OK] Row written successfully!")
        print("="*50)
        print("SUCCESS! GOOGLE SHEETS INTEGRATION IS WORKING")
        print("Please check your Google Sheet for a new row.")
        print("="*50)

    except Exception as e:
        print("\n[ERROR] TEST FAILED:")
        print(e)

if __name__ == "__main__":
    test_google_sheets()
