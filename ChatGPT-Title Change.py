# Reads 1) URLs from Column A and 2) Writes the Current Title Tag to Column B and 3) Recommends a new one and writes it to Column C
# https://docs.google.com/spreadsheets/d/1pSnckqRjqTht9b7AUUfkk3CWvNSVaoGfVRN2TyJCmPE/edit#gid=0
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

# Define function to rename the title tag using ChatGPT
def rename_title_tag(title):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Rename the title tag: {}".format(title),
        max_tokens=30,
        temperature=0.7,
        n=1,
        stop=None
    )
    new_title = response.choices[0].text.strip()
    return new_title

# Access the spreadsheet using the provided URL
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1pSnckqRjqTht9b7AUUfkk3CWvNSVaoGfVRN2TyJCmPE/edit#gid=0'
spreadsheet_id = spreadsheet_url.split('/d/')[1].split('/')[0]
spreadsheet = client.open_by_key(spreadsheet_id)

# Access the "Test 1" sheet
sheet = spreadsheet.worksheet("Test 1")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.google.com/"
}

# Get all values in Column A
urls = sheet.col_values(1)

# Iterate through each URL
for i in range(1, len(urls) + 1):
    url = urls[i - 1]
    try:
        # Set the spoofed User-Agent header
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

        # Get the HTML content of the URL
        response = requests.get(url, headers=headers)
        html_content = response.text

        # Parse the HTML content and extract the title tag
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.title.string.strip() if soup.title else ''

        # Rename the title tag using ChatGPT
        new_title_tag = rename_title_tag(title_tag)

        # Update Column B with the original title tag and Column C with the renamed title tag
        sheet.update_cell(i, 2, title_tag)
        sheet.update_cell(i, 3, new_title_tag)
    except Exception as e:
        print("Error processing URL:", url)
        print(e)

Open AI BigQuery:

from google.cloud import bigquery
from google.oauth2.service_account import Credentials


def fetch_city_items(project_id, dataset_id, table_id, credentials_path):
    credentials = Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(project=project_id, credentials=credentials)
    query = f"SELECT DISTINCT geo.city FROM `{project_id}.{dataset_id}.{table_id}`"
    query_job = client.query(query)
    results = query_job.result()

    city_items = [row.city for row in results]
    prompt
    engineering
    return city_items


def write_to_bigquery(project_id, dataset_id, table_id, data, credentials_path):
    credentials = Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(project=project_id, credentials=credentials)

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)

    errors = client.insert_rows(table, data)

    if errors == []:
        print("Data successfully inserted into BigQuery.")
    else:
        print("Encountered errors while inserting data into BigQuery.")


# Usage
project_id = 'ga4-integration-sandbox'
dataset_id = 'analytics_253079145'
table_id = 'events_20230601'
output_table_id = 'chat-gpt-results'
credentials_path = '/Users/johnoren/PycharmProjects/pythonProject/pythonProject/chatgpt-1/venv/BigQuery-2.json'

# Fetch city items
city_items = fetch_city_items(project_id, dataset_id, table_id, credentials_path)

# Prepare data for BigQuery insertion
data = [{'city': item} for item in city_items]

# Write data to BigQuery table
write_to_bigquery(project_id, dataset_id, output_table_id, data, credentials_path)
