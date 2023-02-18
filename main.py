import os

import requests


# Main Method, runs code
def main():
    auth_token = os.environ["auth_token"]
    course_id = os.environ["course_id"]

    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    url = f'https://bcourses.berkeley.edu/api/v1/courses/{course_id}'
    print(headers, url)
    
    disc_topics = get_discussion_topics(url, headers)
    print(disc_topics)
    result_disc_yes = []
    for topic in (disc_topics):
        print(topic)
        result_disc_yes.append(yes_counter(topic, url, headers))
    print(result_disc_yes)


# Returns a list of discussion topics. Hardcoded right now to be only useful for the berkeley fiction bcourses discussion page.
def get_discussion_topics(url, headers):
    return(requests.get(f'{url}/discussion_topics?scope=unlocked', headers=headers).json())

# Returns a dictionary for yes, no counters for the specific discussion topic
def yes_counter(topic, url, headers):
    topic_id = topic["id"]
    entries = requests.get(f'{url}/discussion_topics/{topic_id}/entries', headers=headers).json()
    yes_counter = 0
    no_counter = 0
    result_counter = {}
    for e in entries:
        message = e["message"]
        first_word = ""
        for i in message:
            if i != " ":
                first_word += i
            else:
                break
        
        if first_word == "YES" or first_word == "yes" or first_word == "Yes":
            yes_counter += 1
        elif first_word == "NO" or first_word == "no" or first_word == "No":
            no_counter += 1
    result_counter["topic"] = topic;
    result_counter["yes"] = yes_counter;
    result_counter["no"] = no_counter;
    return result_counter;
    
# # Runs main method.
# main()

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def build_service():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build("sheets", "v4", credentials=creds)

spreadsheet_id = "1wEGu3snEQlqEahaJ_FMMyYilWYAfykBbvZEwVaQvjiE"
range_name = "A:I"
service = build_service()
res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
