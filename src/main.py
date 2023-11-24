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
from utils_stuff.stats import *

from EMH.Details.DetailsData import DetailsData
from EMH.Summary.SummaryData import SummaryData
from Separated.SeparatedData import SeparatedData
from Separated.Snapshot import Snapshot
from Separated.Player import Player
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
    

    
    
    if game == "gBO":
        rootdir = "../data/{}/".format(match)
        pathData = DATA_PATH + match + "BOData"
        dirList : list[str] = []
        for subdir, dirs, _ in os.walk(rootdir):
            dirList.append(dirs)
        
        nbGameBo = len(dirList[0])
        gameList = dirList[0]

        allSeparatedData : list[SeparatedData] = []
        allSummaryData : list[SummaryData] = []
        allSnapshot15 : list[Snapshot] = []
        allGameStat15 : list[GameStat] = []
        

        for gameIdx in gameList:
            subRootdir = "../data/{}/{}".format(match, gameIdx)
            pathData = DATA_PATH + match + gameIdx + "data"

            summaryDataPath = getSummaryData(subRootdir)
            summaryDataTemp : SummaryData = SummaryData(summaryDataPath)
            separatedDataTemp : SeparatedData = None
            gameStatTemp : GameStat = None
            
            if load :
                
                print("Loading serialized data")
                file = open(pathData, 'rb')
                separatedDataTemp : SeparatedData = pickle.load(file)
                file.close()
            else:
                print("Creating our data")
                separatedDataTemp = SeparatedData(subRootdir + "/Separated")
                file = open(pathData, 'ab')
                pickle.dump(separatedDataTemp, file)
                file.close()
            
            gameDuration : int = summaryDataTemp.gameDuration
            begGameTime : int = separatedDataTemp.begGameTime
            endGameTime : int = separatedDataTemp.endGameTime

            gameStatTemp = GameStat(separatedDataTemp.getSnapShotByTime(900, gameDuration),
                                    gameDuration,
                                    begGameTime,
                                    endGameTime)

            allSeparatedData.append(separatedDataTemp)
            allSnapshot15.append(separatedDataTemp.getSnapShotByTime(900, gameDuration))
            allSummaryData.append(summaryDataTemp)
            allGameStat15.append(gameStatTemp)

        saveDiffStatBO(allGameStat15, "./saved_data", allSnapshot15)

    else :
        subRootdir = "../data/{}/{}".format(match, game)
        summaryDataPath = getSummaryData(subRootdir)
        summaryData : SummaryData = SummaryData(summaryDataPath)
        
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

        firstSplit : SeparatedData = splittedDataset[0]
        print("len unsplited dataset :", len(data.gameSnapshotList))
        print("len first split :", len(firstSplit.gameSnapshotList))

        # print("Ploting position")
        # plotTeamPosition(firstSplit.getPlayerList()[0], firstSplit)

        # print("Creating animation")
        # positionsList : list[list[Position]] = list()
        # i = 0
        
        # for split in splittedDataset:
        #     name = ""
        #     if i < len(splitList):
        #         name = "position_both_teams_{}_{}".format(splitList[i], game)
        #         plotBothTeamsPositionAnimated(split.getPlayerList()[0], split.getPlayerList()[1], split, name)        
        #     i += 1

        snapshot15 = data.getSnapShotByTime(900, gameDuration)
        closestPlayerTeamOne : Player = snapshot15.teamOne.getClosesPlayerToJungler()
        print("Closes player to Oner at 15 min is : {}".format(closestPlayerTeamOne.summonerName))
        jungleProxT1 = getJungleProximity(data, 0)
        print(jungleProxT1)
        jungleProxJDG = getJungleProximity(data, 1)
        print(jungleProxJDG)