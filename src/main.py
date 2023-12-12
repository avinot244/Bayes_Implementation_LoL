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
from utils_stuff.utils_func import getSummaryData, getData
from utils_stuff.Types import *
from utils_stuff.plots.plotsTeam import *
from utils_stuff.stats import *
from utils_stuff.plots.densityPlot import densityPlot
from errorHandling import checkMatchName, checkTeamComposition

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
    parser.add_argument("-d", "--density", action="store_true", default=False, help="Tells if we want to plot the position density. Only with --pathing option")
    parser.add_argument("-g", "--game", metavar="[1|2|3|4|5|BO]", type=str, help="Game to analyse or if we want the whole Best-Off")
    parser.add_argument("-o", "--overview", action="store_true", default=False, help="Compute game stat of players")
    parser.add_argument("-t", "--time", metavar="[time_wanted_in_seconds]", type=int, help="Game time to analyse")
    parser.add_argument("-j", "--jungle-prox", action="store_true", default=False, help="Prints jungle proximity at a given time")
    parser.add_argument("-l", "--load", action="store_true", default=False, help="Tells if we want to load serialized object")
    

    args = parser.parse_args()
    args_data = vars(args)

    pathing = False
    anim = False
    density = False
    game = ""
    overview = False
    time = 0
    load = False
    jungleProximity = False

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
        if arg == "jungle_prox":
            jungleProximity = value
        if arg == "density":
            density = value

    yamlParser : YamlParer = YamlParer("./config.yml")

    assert checkMatchName(yamlParser, DATA_PATH)

    if pathing:
        
        # Loading data of the game
        match = yamlParser.ymlDict['match']
        rootdir = yamlParser.ymlDict['brute_data'] + "{}/g{}".format(match, game)
        # Getting global info of the game
        summaryData : SummaryData = getSummaryData(rootdir)
        (data, gameDuration, begGameTime, endGameTime) = getData(load, yamlParser, game)

        splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
        splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
        if splitList[-1] > gameDuration:
            splitList[-1] = gameDuration
        else:
            splitList.append(gameDuration)
        splittedDataset : list[SeparatedData] = data.splitData(summaryData.gameDuration, splitList)
        
        playerNameListTeamOne = yamlParser.ymlDict['playersTeamOne']
        playerNameListTeamTwo = yamlParser.ymlDict['playersTeamTwo']

        playerNameList = [playerNameListTeamOne, playerNameListTeamTwo]

        assert checkTeamComposition(playerNameList, data)

        if not(os.path.exists(yamlParser.ymlDict['save_path'] + "/Position/{}/".format(yamlParser.ymlDict['match']))):
            os.makedirs(yamlParser.ymlDict['save_path'] + "/Position/{}/".format(yamlParser.ymlDict['match']))
        if anim:
            assert game != "BO"
            print("Ploting pathing with animation of game {} for players {}".format(game, playerNameList))
            if not(os.path.exists("{}/Position/PositionAnimated/{}/g{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'], game))):
                    os.makedirs("{}/Position/PositionAnimated/{}/g{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'], game))
            
            i = 0
            for split in splittedDataset:
                name = ""
                if i < len(splitList):
                    name = "position_both_teams_{}_g{}_{}".format(splitList[i], game, yamlParser.ymlDict['match'])
                    path = "{}/Position/PositionAnimated/{}/g{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'], game)
                    print("saving it to :", path)
                    plotBothTeamsPositionAnimated(playerNameList[0], playerNameList[1], split, name, path)        
                i += 1
        elif density:
            if game != "BO":
                print("Plotting position density of game {} for players {}".format(game, playerNameList))
                if not(os.path.exists("{}/Position/PositionDensity/{}/g{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'], game))):
                    os.makedirs("{}/Position/PositionDensity/{}/g{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'], game))
                save_path = "{}/Position/PositionDensity/{}/g{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'], game)
                
                i = 0
                print([len(split.gameSnapshotList) for split in splittedDataset])
                for split in splittedDataset:
                    graph_name = ""
                    if i < len(splitList):
                        # For team one
                        graph_name = "position_density_teamOne_{}_g{}_{}".format(splitList[i], game, yamlParser.ymlDict['match'])
                        densityPlot(playerNameList[0], graph_name, save_path, split)

                        # For team two
                        graph_name = "position_density_teamTwo_{}_g{}_{}".format(splitList[i], game, yamlParser.ymlDict['match'])
                        densityPlot(playerNameList[1], graph_name, save_path, split)
                    i += 1
        else:
            assert game != "BO"
            print("Plotting pathing without animation of game {} for players {}".format(game, playerNameList))
            i = 0
            for split in splittedDataset:
                name = ""
                if i < len(splitList):
                    name = "position_T1_{}_{}_{}".format(splitList[i], game, yamlParser.ymlDict['match'])
                    path = "{}/Position/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'])
                    plotTeamPosition(playerNameList[0], split, name, path)
                i += 1
            
    elif overview:
        if not(os.path.exists(yamlParser.ymlDict['save_path'] + "/GameStat/OverView/{}/g{}/".format(yamlParser.ymlDict['match'], game))):
            os.makedirs(yamlParser.ymlDict['save_path'] + "/GameStat/OverView/{}/g{}/".format(yamlParser.ymlDict['match'], game))
        if game == "BO":
            print("Computing overvie of the whole Best-Off of match {}".format(yamlParser.ymlDict['match']))
            rootdir = yamlParser.ymlDict['brute_data'] + "{}/".format(yamlParser.ymlDict['match'])
            pathData = yamlParser.ymlDict['serialized_path'] + yamlParser.ymlDict['match'] + "BOData"
            dirList : list[str] = list()
            for subdir, dirs, _ in os.walk(rootdir):
                dirList.append(dirs)
            nbGameBo = len(dirList[0])
            gameList = dirList[0]
            allSeparatedData : list[SeparatedData] = []
            allSummaryData : list[SummaryData] = []
            allSnapshot15 : list[Snapshot] = []
            allGameStat15 : list[GameStat] = []

            for gameIdx in gameList:
                subRootdir = yamlParser.ymlDict['brute_data'] + "/{}/{}".format(yamlParser.ymlDict['match'], gameIdx)
                pathData = yamlParser.ymlDict['brute_data'] + yamlParser.ymlDict['match'] + gameIdx + "data"

                summaryDataTemp : SummaryData = getSummaryData(subRootdir)
                
                gameNumber = gameIdx.split("g")[1]
                (separatedDataTemp, gameDuration, begGameTime, endGameTime) = getData(load, yamlParser, gameNumber)

                if time != None:
                    gameStatTemp = GameStat(separatedDataTemp.getSnapShotByTime(time, gameDuration),
                                            gameDuration,
                                            begGameTime,
                                            endGameTime)

                    allSeparatedData.append(separatedDataTemp)
                    allSnapshot15.append(separatedDataTemp.getSnapShotByTime(time, gameDuration))
                    allSummaryData.append(summaryDataTemp)
                    allGameStat15.append(gameStatTemp)
                else:
                    gameStatTemp = GameStat(separatedDataTemp.getSnapShotByTime(gameDuration, gameDuration),
                                            gameDuration,
                                            begGameTime,
                                            endGameTime)

                    allSeparatedData.append(separatedDataTemp)
                    allSnapshot15.append(separatedDataTemp.getSnapShotByTime(gameDuration, gameDuration))
                    allSummaryData.append(summaryDataTemp)
                    allGameStat15.append(gameStatTemp)

            pathDiffBO = "./saved_data/GameStat/OverView/" + yamlParser.ymlDict['match']
            saveDiffStatBO(allGameStat15, pathDiffBO, allSnapshot15)
        
        else:
            print("Computing overview of game {} at {}".format(game, time))
            (data, gameDuration, begGameTime, endGameTime) = getData(load, yamlParser, game)
            if time != None:
                snapShot : Snapshot = data.getSnapShotByTime(time, gameDuration)
                gameStat : GameStat = GameStat(snapShot, gameDuration, begGameTime, endGameTime)
                path = "{}/GameStat/Overview/{}/g{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'], game)
                saveDiffStatGame(gameStat, "g{}".format(game), path, snapShot)
            else:
                snapShot : Snapshot = data.getSnapShotByTime(gameDuration, gameDuration)
                gameStat : GameStat = GameStat(snapShot, gameDuration, begGameTime, endGameTime)
                path = "{}/GameStat/OverView/{}/g{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'], game)
                saveDiffStatGame(gameStat, "g{}".format(game), path, snapShot)
    
    elif jungleProximity:
        assert game != None
        print("Getting jungle proximity of game {}".format(game))
        (data, gameDuration, begGameTime, endGameTime) = getData(load, yamlParser, game)

        splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
        if splitList[-1] > gameDuration:
            splitList[-1] = gameDuration
        else:
            splitList.append(gameDuration)
        splittedDataset : list[SeparatedData] = data.splitData(gameDuration, splitList)
        
        teamNames = data.getTeamNames()

        jungleProxList : list = list()
        print(len(splittedDataset))
        for splitData in splittedDataset:
            jungleProxList.append(getJungleProximity(splitData, teamNames['T1']))
        
        print(jungleProxList)