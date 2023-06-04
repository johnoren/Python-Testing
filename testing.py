import gspread
from google.oauth2.service_account import Credentials
from bs4 import BeautifulSoup
import requests
import openai

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('/Users/johnoren/PycharmProjects/pythonProject/pythonProject/chatgpt-1/venv/Google Sheets 1.json', scopes=scope)
client = gspread.authorize(creds)

# Set up OpenAI API credentials
openai.api_key = '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'

# Access the spreadsheet using the provided URL
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1pSnckqRjqTht9b7AUUfkk3CWvNSVaoGfVRN2TyJCmPE/edit#gid=0'
spreadsheet_id = spreadsheet_url.split('/d/')[1].split('/')[0]
spreadsheet = client.open_by_key(spreadsheet_id)

# Access the "Test 1" sheet
sheet = spreadsheet.worksheet("Test 1")

# Add column titles if they don't exist
column_titles = sheet.row_values(1)
if len(column_titles) < 3:
    sheet.update_cell(1, 1, "URLs")
    sheet.update_cell(1, 2, "Current Title")
    sheet.update_cell(1, 3, "AI Recommendation")

# Get all values in Column A starting from line 2
urls = sheet.col_values(1)[1:]

# Set headers with Chrome user agent and referrer from Google
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.google.com/"
}

# Define function to rename the title tag using OpenAI
def rename_title_tag(title):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Provide a title tag that follows best SEO practices and has a consistent structure for the following title tag: '{}'\n\nNew title tag:".format(title),
        max_tokens=30,
        temperature=0.7,
        n=1,
        stop=None
    )
    new_title = response.choices[0].text.strip()
    new_title = new_title.replace("<title>", "").replace("</title>", "")
    return new_title

# Iterate through each URL
for i, url in enumerate(urls, start=2):
    try:
        # Get the HTML content of the URL with headers
        response = requests.get(url, headers=headers)
        html_content = response.text

        # Parse the HTML content and extract the title tag
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.title.string.strip() if soup.title else ''

        # Rename the title tag using OpenAI
        new_title_tag = rename_title_tag(title_tag)

        # Update Column B with the title tag
        sheet.update_cell(i, 2, title_tag)

        # Update Column C with the recommended new title tag
        sheet.update_cell(i, 3, new_title_tag)

    except Exception as e:
        print("Error processing URL:", url)
        print(e)
