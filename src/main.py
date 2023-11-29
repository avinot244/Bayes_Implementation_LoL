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
from YamlParser import YamlParer




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-p", "--pathing", action="store_true", default=False, help="Tells if we want to print pathing of players")
    parser.add_argument("-a", "--anim", action="store_true", default=False, help="Tells if we want to plot animations. Only with --pathing option")
    parser.add_argument("-g", "--game", metavar="[1|2|3|4|5|BO]", type=str, help="Game to analyse or if we want the whole Best-Off")
    parser.add_argument("-o", "--overview", action="store_true", default=False, help="Compute game stat of players")
    parser.add_argument("-t", "--time", metavar="[time_wanted_in_seconds]", type=int, help="Game time to analyse")
    parser.add_argument("-l", "--load", action="store_true", default=False, help="Tells if we want to load serialized object")
    

    args = parser.parse_args()
    args_data = vars(args)

    pathing = False
    anim = False
    game = ""
    overview = False
    time = 0
    load = False

    for arg, value in args_data.items():
        if arg == "pathing":
            pathing = value
        if arg == "anim":
            anim = value
        if arg == "game":
            game = value
        if arg == "overview":
            overview = value
        if arg == "time":
            time = value
        if arg == "load":
            load = value

    yamlParser : YamlParer = YamlParer("./config.yml")

    if pathing:
        assert game != "BO"
        
        # Loading data of the game
        match = yamlParser.ymlDict['match']
        rootdir = yamlParser.ymlDict['brute_data'] + "{}/g{}".format(match, game)
        summaryDataPath = getSummaryData(rootdir)
        summaryData : SummaryData = SummaryData(summaryDataPath)

        pathData = yamlParser.ymlDict['serialized_path'] + match + "g{}".format(game) + 'data'
        data : SeparatedData = None
        if load :
            print("Loading serialized data")
            file = open(pathData, 'rb')
            data : SeparatedData = pickle.load(file)
            file.close()
        else :
            data = SeparatedData(rootdir + "/Separated")
            pathData = DATA_PATH + match + game + "data"
            file = open(pathData, 'ab')
            pickle.dump(data, file)
            file.close()
        
        # Getting global info of the game
        gameDuration : int = summaryData.gameDuration
        begGameTime : int = data.begGameTime
        endGameTime : int = data.endGameTime
        splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
        splitList.append(gameDuration)
        splittedDataset : list[SeparatedData] = data.splitData(summaryData.gameDuration, splitList)
        
        playerNameListTeamOne = yamlParser.ymlDict['playersTeamOne']
        playerNameListTeamTwo = yamlParser.ymlDict['playersTeamTwo']
        print(playerNameListTeamOne, playerNameListTeamTwo)
        playerNameList = [playerNameListTeamOne, playerNameListTeamTwo]
        # TODO : Make assertions to check if players parsed in yml file are in each teams
        if anim:
            print("Ploting pathing with animation of game {} for players {}".format(game, playerNameList))
            i = 0
            for split in splittedDataset:
                name = ""
                if i < len(splitList):
                    name = "position_both_teams_{}_g{}".format(splitList[i], game)
                    plotBothTeamsPositionAnimated(playerNameList[0], playerNameList[1], split, name)        
                i += 1
        else:
            print("Plotting pathing without animation of game {} for players {}".format(game, playerNameList))
            i = 0
            for split in splittedDataset:
                name = ""
                if i < len(splitList):
                    name = "position_T1_{}_{}".format(splitList[i], game)
                    plotTeamPosition(playerNameList[0], split, name)        
                i += 1
            
    elif overview:
        print("Computing overview of game {} at {}".format(game, time))
    
    
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


# snapshot15 = data.getSnapShotByTime(900, gameDuration)
# closestPlayerTeamOne : Player = snapshot15.teamOne.getClosesPlayerToJungler()
# print("Closes player to Oner at 15 min is : {}".format(closestPlayerTeamOne.summonerName))
# jungleProxT1 = getJungleProximity(data, 0)
# print(jungleProxT1)
# jungleProxJDG = getJungleProximity(data, 1)
# print(jungleProxJDG)