

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_URL = os.getenv("SHEET_URL")
GOOGLE_CREDENTIALS_JSON = "google-credentials.json"

def get_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_JSON, scope)
    client = gspread.authorize(creds)
    return client.open_by_url(SHEET_URL)

def get_sheet_data():
    sheet = get_sheet().sheet1
    return sheet.get_all_records()

def get_categories():
    records = get_sheet_data()
    return sorted({row.get("Category", "") for row in records if row.get("Category", "")})

def append_order(record: dict):
    order_sheet = get_sheet().worksheet("Orders")
    order_sheet.append_row(list(record.values()))

def update_stock(product_name: str, delta: int):
    sheet = get_sheet().sheet1
    records = sheet.get_all_records()
    headers = sheet.row_values(1)
    stock_index = headers.index("Stock") + 1
    for i, row in enumerate(records, start=2):
        if row.get("Product") == product_name:
            current_stock = int(row.get("Stock", 0))
            sheet.update_cell(i, stock_index, current_stock + delta)
            break