import requests
import os
from datetime import datetime
from get_token import get_token

# requesting access token with the help of the get_token.py module
token = get_token()

print("yo")
# creating query string. We want to set "matchDateFrom" to the beginning of today
today = datetime.now()
today = datetime(today.year, today.month, today.day)  # truncating time
querystring = {"matchDateFrom": today.isoformat() + 'Z'}  # 'Z' stands for UTC

# requesting the /matches endpoint
response = requests.get(
    'https://lolesports-api.bayesesports.com/v2/games/LOLTMNT03_22191/download?option=GAMH_SEPARATED',
    headers={"Authorization": f"Bearer {token}"},
    params=querystring
)
if response.status_code != 200:
    response.raise_for_status()

result = response.json()

print("Url to download GAMH_SEPARATED: ", result["url"])