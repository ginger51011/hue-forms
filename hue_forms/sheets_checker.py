#!/usr/bin/env python3
from __future__ import print_function
import pickle
import os.path as path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
TOKEN_PATH = path.join(path.expanduser("~"), "./.config/hue-forms/token.pickle")
CREDENTIALS_PATH = path.join(path.expanduser("~"), "./.config/hue-forms/credentials.json")
RANGE = "B:B" # B är färg, A är timestamp. This is whole row

def check_leader(sheet_id):
    """
    Basically taken from google python quickstart,
    but edited
    """
    creds = None

    if path.exists(TOKEN_PATH):
        if path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    # Kallar API:n
    sheet = service.spreadsheets()
    results = sheet.values().get(spreadsheetId=sheet_id, range=RANGE).execute()
    values = results.get('values', [])

    leader = ""

    if not values:
        return
    else:   # We find the leader
        # Construct leaderboard by number of entries
        leaderboard = {}
        for row in values:
            choice = row[0]
            if choice not in leaderboard:
                leaderboard[choice] = 1
            else:
                leaderboard[choice] = leaderboard[choice] + 1
        
        # Finx max number of entries in leaderboard
        leader_value = 0
        for choice in leaderboard:
            if leaderboard[choice] > leader_value:
                leader = choice
                leader_value = leaderboard[choice]
            else:
                continue  
    
    return leader