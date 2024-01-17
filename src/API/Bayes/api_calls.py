import requests
import os
import zipfile, io
from datetime import datetime
from enum import Enum
import urllib.request
import json
import shutil

from API.Bayes.get_token import get_token


def get_games_by_page(page : int, gameType : str, patch : str, tournaments : str) -> list:
    token = get_token()
    if tournaments != "":
        querystring = {"type": gameType, "page" : page, "tags": tournaments}
    else:
        querystring = {"type": gameType, "page" : page}

    response = requests.get(
        'https://lolesports-api.bayesesports.com/v2/games',
        headers={"Authorization" : "Bearer {}".format(token)},
        params=querystring
    )
    if response.status_code != 200:
        response.raise_for_status()
    result : dict = response.json()
    

    platformGameIdList : list = list()
    for game in result['items']:
        if patch != "":
            gameVersion = game['gameVersion'].split('.')[0] + game['gameVersion'].split('.')[1]
            patchVersion = patch.split(".")[0] + patch.split(".")[1]
            if gameVersion == patchVersion:
                platformGameIdList.append(game['platformGameId'])
        else:
            platformGameIdList.append(game['platformGameId'])
    
    return platformGameIdList

def get_games_by_date(begDate : str, endDate : str, gameType : str) -> list:
    token = get_token()
    querystring = {"type" : gameType,
                   "from": begDate,
                   "to": endDate}
    response = requests.get(
        'https://lolesports-api.bayesesports.com/v2/games',
        headers={"Authorization" : "Bearer {}".format(token)},
        params=querystring
    )
    if response.status_code != 200:
        response.raise_for_status()
    result : dict = response.json()

    platformGameIdList : list = list()

    for games in result['items']:
        platformGameIdList.append(games['platformGameId'])    
    return platformGameIdList

def get_game_by_playerName(playerName : str, gameType : str) -> list:
    token = get_token()
    querystring = {"type" : gameType,
                   "playerName" : playerName}
    response = requests.get(
        'https://lolesports-api.bayesesports.com/v2/games',
        headers={"Authorization" : "Bearer {}".format(token)},
        params=querystring
    )
    if response.status_code != 200:
        response.raise_for_status
    result : dict = response.json()

    platformGameIdList : list = list()
    
    for games in result['items']:
        platformGameIdList.append(games['platformGameId'])
    
    return platformGameIdList


def get_download_link(platformGameId : str, downloadOption : str) -> str:
    token = get_token()
    querystring = {"option" : downloadOption}
    response = requests.get(
        'https://lolesports-api.bayesesports.com/v2/games/{}/download'.format(platformGameId),
        headers={"Authorization" : "Bearer {}".format(token)},
        params=querystring
    )
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()['url']


def save_downloaded_file(url : str, path : str, name : str, downloadOption : str):
    print("Saving {} with {} download".format(name, downloadOption))
    response = requests.get(url)
    if downloadOption == "HISTORIC_BAYES_SEPARATED": 
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall("{}".format(path))

    elif downloadOption == "GAMH_SUMMARY":
        with urllib.request.urlopen(url) as dlLink:
            data = json.load(dlLink)
            with open('{}/{}_SUMMARY.json'.format(path, name), 'w') as f:
                json.dump(data, f)
    elif downloadOption == "GAMH_DETAILS":
        with urllib.request.urlopen(url) as dlLink:
            data = json.load(dlLink)
            with open('{}/{}_DETAILS.json'.format(path, name), 'w') as f:
                json.dump(data, f)