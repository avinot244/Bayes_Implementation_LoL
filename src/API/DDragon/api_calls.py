import requests
import os
import zipfile, io
from datetime import datetime
from enum import Enum
import urllib.request
import json
import shutil

def get_champion_mapping_key():
    response = requests.get(
        'https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json'
    )

    if response.status_code != 200:
        response.raise_for_status()
    res : dict = dict()
    
    for championName, data in response.json()['data'].items():
        res[data['key']] = championName
    
    return res

def get_item_mapping_key():
    response = requests.get(
        'https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/item.json'
    )

    if response.status_code != 200:
        response.raise_for_status()

    res : dict = dict()
    for itemKey, data in response.json()['data'].items():
        res[itemKey] = data['name']
    
    return res