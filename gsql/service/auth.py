from __future__ import print_function
from googleapiclient.discovery import build
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

ROOT_DIR = ""
# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(ROOT_DIR + "token.json"):
        creds = Credentials.from_authorized_user_file(ROOT_DIR + "token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open(ROOT_DIR + "token.json", "w") as token:
            token.write(creds.to_json())
    gsheet_service = build(serviceName="sheets", version="v4", credentials=creds)
    gdrive_service = build(serviceName="drive", version="v2", credentials=creds)
    return creds, gsheet_service, gdrive_service
