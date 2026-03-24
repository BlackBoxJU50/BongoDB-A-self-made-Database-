import gspread
import sys
import os

# Add root to path for config import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# SPREADSHEET_ID will be injected at runtime

class BongoCollection:
    def __init__(self, spreadsheet, name, headers):
        self.spreadsheet = spreadsheet
        self.name = name
        self.headers = headers
        self.sheet = self.get_or_create()

    def get_or_create(self):
        try:
            sheet = self.spreadsheet.worksheet(self.name)
            # Ensure headers are correct if sheet exists
            curr_headers = sheet.row_values(1)
            if not curr_headers or curr_headers != self.headers:
                sheet.update('A1', [self.headers])
            return sheet
        except gspread.exceptions.WorksheetNotFound:
            # Auto-Setup for new collections
            sheet = self.spreadsheet.add_worksheet(title=self.name, rows=1000, cols=max(20, len(self.headers)))
            sheet.update('A1', [self.headers])
            return sheet

    def insert(self, data_list):
        self.sheet.append_row(data_list)

    def find_all(self):
        # Use expected_headers to avoid 'duplicate empty column' errors
        return self.sheet.get_all_records(expected_headers=self.headers)

    def find_one(self, key, value):
        records = self.find_all()
        for i, record in enumerate(records):
            if str(record.get(key)) == str(value):
                record['_row'] = i + 2 # Add row number (1-based + 1 for header)
                return record
        return None

    def update(self, key, value, new_data_dict):
        record = self.find_one(key, value)
        if not record: return False
        
        row_num = record['_row']
        row_data = []
        for h in self.headers:
            row_data.append(new_data_dict.get(h, record.get(h, '')))
            
        self.sheet.update(f'A{row_num}', [row_data])
        return True

    def delete(self, key, value):
        record = self.find_one(key, value)
        if not record: return False
        self.sheet.delete_rows(record['_row'])
        return True

class BongoDB:
    def __init__(self, credentials, spreadsheet_id):
        self.client = gspread.authorize(credentials)
        self.spreadsheet = self.client.open_by_key(spreadsheet_id)
        
    def collection(self, name, headers):
        return BongoCollection(self.spreadsheet, name, headers)
