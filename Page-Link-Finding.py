import gspread
from google.oauth2.service_account import Credentials
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('/Users/johnoren/PycharmProjects/pythonProject/pythonProject/Python-Testing/venv/Google Sheets 1.json', scopes=scope)
client = gspread.authorize(creds)

# Access the spreadsheet using the provided URL
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1pSnckqRjqTht9b7AUUfkk3CWvNSVaoGfVRN2TyJCmPE/edit#gid=0'
spreadsheet_id = spreadsheet_url.split('/d/')[1].split('/')[0]
spreadsheet = client.open_by_key(spreadsheet_id)

# Access the "Test 2" sheet
sheet = spreadsheet.worksheet("Test 2")

# Update headers for Column A, B, C, D, and E
sheet.update_cell(1, 1, "Website")
sheet.update_cell(1, 2, "Link")
sheet.update_cell(1, 3, "Link Found")
sheet.update_cell(1, 4, "Server Response")
sheet.update_cell(1, 5, "Timestamp")

# Get the values in Column A (URLs) and Column B (links)
urls = sheet.col_values(1)
links = sheet.col_values(2)

# Start the review from the second row available
start_row = 2

# Iterate through the rows of the sheet starting from row 2
for i in range(start_row, len(urls) + 1):
    url = urls[i - 1]
    link = links[i - 1]
    try:
        # Set the spoofed User-Agent header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.google.com/"
        }

        # Get the HTML content of the URL with spoofed headers
        response = requests.get(url, headers=headers)
        html_content = response.text

        # Check if the link is present in the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        link_found = False
        for a_tag in soup.find_all('a', href=True):
            if link in a_tag['href']:
                link_found = True
                break

        # Get the server header response code
        response_code = response.status_code

        # Update "Test 2" sheet based on the link presence and response code
        if link_found:
            sheet.update_cell(i, 3, "Yes")
        else:
            sheet.update_cell(i, 3, "No")
        sheet.update_cell(i, 4, response_code)

        # Set GMT timestamp in Column E
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S GMT")
        sheet.update_cell(i, 5, timestamp)

    except Exception as e:
        print("Error processing row", i)
        print(e)
