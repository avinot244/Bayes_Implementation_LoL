import requests
from datetime import datetime, timedelta
import json
import os
from getpass import getpass

def portal_login(username : str, password : str) -> dict:
    url = 'https://lolesports-api.bayesesports.com/v2/auth/login'
    headers = {"Content-Type": "application/json"}
    creds = {'username': username, 'password': password}
    response = requests.post(url, json=creds, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def store_token(response_token: dict, filename: str):
    result = dict(response_token)  # create a copy of the input dict
    expire_date = datetime.now() + timedelta(seconds=result.pop('expiresIn'))
    result['expiresAt'] = expire_date.timestamp()
    with open(filename, 'w') as f:
        json.dump(result, f)

def is_stored_token_fresh(stored_token: dict) -> bool:
    expire_date = datetime.fromtimestamp(stored_token['expiresAt'])
    return datetime.now() < expire_date

def get_token_from_file(filename: str):
    if not os.path.exists(filename):
        return None
    with open(filename) as f:
        stored_token = json.load(f)
    if is_stored_token_fresh(stored_token):
        return stored_token['accessToken']
    else:
        return None
    
def get_token() -> str:
    filename = 'token.json'
    token = get_token_from_file(filename)
    if token is None:
        # stored token is expired, asking user for credentials
        username = input(f'Portal login: ')
        password = getpass(f'Password for {username}: ')
        # requesting a new token from API
        response_token = portal_login(username, password)
        # storing the token details
        store_token(response_token, filename)
        token = response_token['accessToken']
    return token