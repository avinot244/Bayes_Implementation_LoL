import json
import pandas as pd
import numpy as np
import math
import os
import re
import pickle

from utils_stuff.globals import *
from EMH.Summary.SummaryData import SummaryData
from YamlParser import YamlParer
from Separated.SeparatedData import SeparatedData


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

def getData(load : bool,
             yamlParser : YamlParer,
             game : str):
    match = yamlParser.ymlDict['match']
    rootdir = yamlParser.ymlDict['brute_data'] + "{}/g{}".format(match, game)
    summaryData = getSummaryData(rootdir)

    pathData = yamlParser.ymlDict['serialized_path'] + match + "g{}data".format(game)
    data : SeparatedData = None
    if load :
        print("Loading serialized data")
        file = open(pathData, 'rb')
        data : SeparatedData = pickle.load(file)
        file.close()
    else :
        data = SeparatedData(rootdir + "/Separated")
        pathData = DATA_PATH + match + "g{}".format(game) + "data"
        file = open(pathData, 'ab')
        pickle.dump(data, file)
        file.close()
    
    gameDuration : int = summaryData.gameDuration
    begGameTime : int = data.begGameTime
    endGameTime : int = data.endGameTime
    return (data, gameDuration, begGameTime, endGameTime)