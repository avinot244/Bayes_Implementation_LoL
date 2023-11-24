# clear && python3 main.py --match NORDvsBRUTE --game 1 --file DETAILS
# clear && python3 main.py --match JDGvsT1 --game 1 --file DETAILS
from tqdm import tqdm

import argparse
import os
import json
import pandas as pd
import pickle
import datetime

from utils_stuff.globals import *
from utils_stuff.utils_func import *
from utils_stuff.Types import *
from utils_stuff.plots import *
from utils_stuff.statDiff import *

from EMH.Details.DetailsData import DetailsData
from EMH.Summary.SummaryData import SummaryData
from Separated.SeparatedData import SeparatedData
from Separated.Snapshot import Snapshot
from GameStat import GameStat




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--match", metavar="[NORDvsBRUTE]", required=True, help="Match to analyse")
    parser.add_argument("-g", "--game", metavar="[1|2|3|4|5|BO]", required=True, help="Game to analyse")
    parser.add_argument("-f", "--file", metavar="[DETAILS | SUMMARY]", required=True, help="If you want to have summary or detail json loaded")
    parser.add_argument("-l", "--load", action="store_true", default=False, help="Load serilized object linked to inputs")

    args = parser.parse_args()
    args_data = vars(args)

    match = ""
    game = ""
    file = ""
    load = False

    for arg, value in args_data.items():
        if arg == "match":
            match = value
        if arg == "game":
            game = "g{}".format(value)
        if arg == "file":
            file = value
        if arg == "load":
            load = value
    

    path = DATA_PATH + match + "/" + game + "/" + "ESPORTSTMNT03_3228025_SUMMARY.json"
    summaryData : SummaryData = SummaryData(path)
    
    if game == "gBO":
        rootdir = "../data/{}/".format(match)
        pathData = DATA_PATH + match + "BOData"
        
        
        data : SeparatedData = None
        

    
    else :
        rootdir = '../data/{}/{}/Separated'.format(match, game)
        pathData = DATA_PATH + match + game + "data"
        data : SeparatedData = None
        if load :
            print("Loading serialized data")
            file = open(pathData, 'rb')
            data : SeparatedData = pickle.load(file)
            file.close()
        else :
            data = SeparatedData(rootdir)
            pathData = DATA_PATH + match + game + "data"
            file = open(pathData, 'ab')
            pickle.dump(data, file)
            file.close()
        

        gameDuration : int = summaryData.gameDuration
        begGameTime : int = data.begGameTime
        endGameTime : int = data.endGameTime

        splitList = [300, 900, gameDuration]
        splittedDataset : list[SeparatedData] = data.splitData(summaryData.gameDuration, splitList)

        firstSplit = splittedDataset[0]
        print("len unsplited dataset :", len(data.gameSnapshotList))
        print("len first split :", len(firstSplit.gameSnapshotList))

        print("Ploting position")
        plotTeamPosition(firstSplit.getPlayerList()[0], firstSplit)

        print("Creating animation")
        positionsList : list[list[Position]] = list()
        # i = 0
        
        # for split in splittedDataset:
        #     name = ""
        #     if i < len(splitList):
        #         name = "position_both_teams_{}_{}".format(splitList[i], game)
        #         plotBothTeamsPositionAnimated(split.getPlayerList()[0], split.getPlayerList()[1], split, name)        
        #     i += 1

        snapshot15 = data.getSnapShotByTime(900, gameDuration)
        print(snapshot15.convertGameTimeToSeconds(gameDuration, data.begGameTime, data.endGameTime))
        gameStat15 : GameStat = GameStat(snapShot=snapshot15, gameDuration=gameDuration, begGameTime=begGameTime, endGameTime=endGameTime)

        saveDiffStatGame(gameStat15, game, "./", snapshot15)