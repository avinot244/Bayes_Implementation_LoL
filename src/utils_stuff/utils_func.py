import json
import pandas as pd
import numpy as np
import math
import os
import re
import pickle
import yaml
import time
import shutil

from utils_stuff.globals import *
from EMH.Summary.SummaryData import SummaryData
from YamlParser import YamlParser
from Separated.Game.SeparatedData import SeparatedData


def get_all_event_types(json_path_details:str) -> dict:
    with open(json_path_details, 'r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data)
    frames = df['frames'][0]
    
    unique_event_type : dict = dict()
    for frame in frames: # Looping throug every frame snapshot
        events = frame['events']
        for event in events: # Looping throug every event of that snapshot
            event_attributes = list(event.keys())
            if not(event['type'] in list(unique_event_type.keys())):
                unique_event_type[event['type']] = event_attributes
        
    
    for (_, v) in unique_event_type.items():
        v.remove('type')
    
    return unique_event_type
        


def getSummaryData(rootdir : str) -> SummaryData:
    for subdir, _, files in os.walk(rootdir):
        for file in files:
            x = re.search("SUMMARY", file)
            if x != None:
                return SummaryData(os.path.join(subdir, file))

def getData(yamlParser : YamlParser,
            idx : int):
    match = yamlParser.ymlDict['match'][idx]
    rootdir = yamlParser.ymlDict['brute_data'] + "{}".format(match)
    summaryData = getSummaryData(rootdir)

    pathData = yamlParser.ymlDict['serialized_path'] + match + "data"
    data : SeparatedData = None

    if not(os.path.exists(pathData)):
        print("Parsing Json files")
        data = SeparatedData(rootdir + "/Separated")
        pathData = DATA_PATH + match + "data"
        file = open(pathData, 'ab')
        pickle.dump(data, file)
        file.close()
    else:
        if os.path.exists(yamlParser.ymlDict['serialized_path'] + match):
            print("Removing Json files")
            # shutil.rmtree(yamlParser.ymlDict['brute_data'] + match + "/Separated/")
        print("Loading serialized data")

        file = open(pathData, 'rb')
        data : SeparatedData = pickle.load(file)
        file.close()
        
    gameDuration : int = summaryData.gameDuration
    begGameTime : int = data.begGameTime
    endGameTime : int = data.endGameTime
    return (data, gameDuration, begGameTime, endGameTime)


def getUnsavedGameNames(gameNames : list[str], path : str) -> list[str]:
    res = []
    presentGameNames = []
    for root, _, _ in os.walk(path, topdown=False):
        presentGameNames.append(root.split("/")[2])

    for gameName in gameNames:
        if not(gameName in presentGameNames):
            res.append(gameName)
    return res

def replaceMatchName(gameNames : list[str], path : str):
    try:
        # Try to read existing data
        try:
            with open(path, 'r') as file:
                existing_data = yaml.safe_load(file)
        except FileNotFoundError:
            existing_data = {}

        # Assign the new list to the field
        existing_data["match"] = gameNames

        # Write the updated data back to the file
        with open(path, 'w') as file:
            yaml.safe_dump(existing_data, file)

        print(f"YAML file successfully updated or created at '{path}'.")
    except Exception as e:
        print(f"Error: {e}")

def write_yaml_file(data, file_path):
    try:
        # Try to read existing data
        try:
            with open(file_path, 'r') as file:
                existing_data = yaml.safe_load(file)
        except FileNotFoundError:
            existing_data = {}

        # Update existing data with new data
        existing_data.update(data)

        # Write the combined data back to the file
        with open(file_path, 'w') as file:
            yaml.safe_dump(existing_data, file)

    except Exception as e:
        print(f"Error: {e}")
    

def getRole(data : SeparatedData, summonnerName : str = None, participantID : int = None):
    if summonnerName != None:
        participantID = data.getPlayerID(summonnerName)
    
    if data.gameSnapshotList[0].teamOne.isPlayerInTeam(participantID):
        participantIdx = data.gameSnapshotList[0].teamOne.getPlayerIdx(participantID)
        return roleMap[participantIdx]
    elif data.gameSnapshotList[0].teamTwo.isPlayerInTeam(participantID):
        participantIdx = data.gameSnapshotList[0].teamTwo.getPlayerIdx(participantID)
        return roleMap[participantIdx]
