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
from utils_stuff.utils_func import getSummaryData, getData, getUnsavedGameNames, replaceMatchName
from utils_stuff.Types import *
from utils_stuff.plots.plotsTeam import *
from utils_stuff.stats import *
from utils_stuff.plots.densityPlot import densityPlot
from errorHandling import checkMatchName, checkTeamComposition

from EMH.Details.DetailsData import DetailsData
from EMH.Summary.SummaryData import SummaryData
from Separated.Game.SeparatedData import SeparatedData
from Separated.Game.Snapshot import Snapshot
from Separated.Game.Player import Player
from GameStat import GameStat
from YamlParser import YamlParser
from API.Bayes.api_calls import get_games_by_date, get_games_by_page, save_downloaded_file, get_download_link
from Separated.Draft.Draft import Draft
from draftDBQueries.getPlayerPicks import getPlayerPicks
from downloader import downloadGames




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-p", "--pathing", action="store_true", default=False, help="Tells if we want to print pathing of players")
    parser.add_argument("-a", "--anim", action="store_true", default=False, help="Tells if we want to plot animations. Only with --pathing option")
    parser.add_argument("-d", "--density", action="store_true", default=False, help="Tells if we want to plot the position density. Only with --pathing option")
   
    parser.add_argument("-o", "--overview", action="store_true", default=False, help="Compute game stat of players")
    parser.add_argument("-gr", "--graph", action="store_true", default=False, help="Tells if we want to plot the stats")
    parser.add_argument("-t", "--time", metavar="[time_wanted_in_seconds]", type=int, help="Game time to analyse")
    
    parser.add_argument("-j", "--jungle-prox", action="store_true", default=False, help="Prints jungle proximity at a given time")
    parser.add_argument("-l", "--load", action="store_true", default=False, help="Tells if we want to load serialized object")
    
    parser.add_argument("-dl", "--download", action="store_true", default=False, help="Tells if we want to download game data from api")
    parser.add_argument("-dB", "--dateBeg", metavar="[YYYY-MM-DD]", type=str, help="Beginning date of when we extract game")
    parser.add_argument("-dE", "--dateEnd", metavar="[YYYY-MM-DD]", type=str, help="End date of when we extract game")
    parser.add_argument("-gT", "--game-type", metavar="[ESPORTS, SCRIM, CHAMPIONS_QUEUE, GENERIC]", type=str, help="Game type we want to download")
    parser.add_argument("-dlO", "--download-option", metavar="[GAMH_DETAILS, GAMH_SUMMARY, ROFL_REPLAY, HISTORIC_BAYES_SEPARATED, HISTORIC_BAYES_DUMP]", type=str, help="Type of data we want to downoad form the game")
    parser.add_argument("-n", "--number", metavar="[Amounf_of_game_wanted]", type=int, help="Amount of game we want to download")
    parser.add_argument("-f", "--from", metavar="[page_number]", type=int, help="Page number from where we get data")

    parser.add_argument("-pr", "--pick-rate", metavar="[player_name]", type=str, help="Name of the player we want to get pick rate")
    parser.add_argument("-qr", "--querry", metavar="[player_name]", type=str, help="Gets the pickrate of each champion of the given player")

    args = parser.parse_args()
    args_data = vars(args)

    pathing = False
    anim = False
    density = False
    overview = False
    time = 0
    load = False
    jungleProximity = False
    graph = False
    download = False
    dateBeg, dateEnd = ("", "")
    gameType = ""
    draft = False
    querry = ""
    number = -1
    fromPage = 0

    for arg, value in args_data.items():
        if arg == "pathing":
            pathing = value
        if arg == "anim":
            anim = value
        if arg == "overview":
            overview = value
        if arg == "graph":
            graph = value
        if arg == "time":
            time = value
        if arg == "load":
            load = value
        if arg == "jungle_prox":
            jungleProximity = value
        if arg == "density":
            density = value
        if arg == "download":
            download = value
        if arg == "dateBeg":
            dateBeg = value
        if arg == "dateEnd":
            dateEnd = value
        if arg == "game_type":
            gameType = value
        if arg == "draft":
            draft = value
        if arg == "querry":
            querry = value
        if arg == "number":
            number = value
        if arg == "from":
            fromPage = value

    yamlParser : YamlParser = YamlParser("./config.yml")
    if not(download):
        assert checkMatchName(yamlParser, DATA_PATH)

    if pathing:
        # Loading data of the game
        assert len(yamlParser.ymlDict['match']) == 1

        match = yamlParser.ymlDict['match'][0]
        rootdir = yamlParser.ymlDict['brute_data'] + "{}/".format(match)
        # Getting global info of the game
        summaryData : SummaryData = getSummaryData(rootdir)
        (data, gameDuration, begGameTime, endGameTime) = getData(load, yamlParser, idx=0)

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

        if not(os.path.exists(yamlParser.ymlDict['save_path'] + "/Position/{}/".format(yamlParser.ymlDict['match'][0]))):
            os.makedirs(yamlParser.ymlDict['save_path'] + "/Position/{}/".format(yamlParser.ymlDict['match'][0]))
        if anim:
            print("Ploting pathing with animation of game {} for players {}".format(yamlParser.ymlDict['match'][0], playerNameList))
            if not(os.path.exists("{}/Position/PositionAnimated/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))):
                    os.makedirs("{}/Position/PositionAnimated/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))
            
            i = 0
            for split in splittedDataset:
                name = ""
                if i < len(splitList):
                    name = "position_both_teams_{}}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                    path = "{}/Position/PositionAnimated/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
                    print("saving it to :", path)
                    plotBothTeamsPositionAnimated(playerNameList[0], playerNameList[1], split, name, path)        
                i += 1
        elif density:
            if len(yamlParser.ymlDict['match']) == 1:
                print("Plotting position density of game {} for players {}".format(yamlParser.ymlDict['match'][0], playerNameList))
                if not(os.path.exists("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))):
                    os.makedirs("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))
                save_path = "{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
                
                i = 0
                for split in splittedDataset:
                    graph_name = ""
                    if i < len(splitList):
                        # For team one
                        graph_name = "position_density_teamOne_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                        densityPlot(playerNameList[0], graph_name, save_path, split)

                        # For team two
                        graph_name = "position_density_teamTwo_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                        densityPlot(playerNameList[1], graph_name, save_path, split)
                    i += 1
        else:
            assert len(yamlParser.ymlDict['match']) == 1
            print("Plotting pathing without animation of game {} for players {}".format(yamlParser.ymlDict['match'][0], playerNameList))
            i = 0
            for split in splittedDataset:
                name = ""
                if i < len(splitList):
                    name = "position_T1_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                    path = "{}/Position/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
                    plotTeamPosition(playerNameList[0], split, name, path)
                i += 1
            
    elif overview:
        if not(os.path.exists(yamlParser.ymlDict['save_path'] + "/GameStat/OverView/{}/".format(yamlParser.ymlDict['match'][0]))):
            os.makedirs(yamlParser.ymlDict['save_path'] + "/GameStat/OverView/{}/".format(yamlParser.ymlDict['match'][0]))
        if graph:
            if yamlParser.ymlDict['match'] > 1:
                print("Plotting overview of th whole Best-Of of match {}".format(yamlParser.ymlDict['match']))
            else:
                print("Plotting overview of at {} for match {}".format(time, yamlParser.ymlDict['match'][0]))
                (data, gameDuration , begGameTime, endGameTime) = getData(load, yamlParser, idx=0)
                if time != None:
                    snapShot : Snapshot = data.getSnapShotByTime(time, gameDuration)
                    gameStat : GameStat = GameStat(snapShot, gameDuration, begGameTime, endGameTime)
                    path = "{}/GameStat/Overview/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
                    #TODO : do graph stuff

                    plotDiffStatGame(gameStat, path, snapShot)
                    
        else :
            if yamlParser.ymlDict['match'] > 1:
                print("Computing overview of the whole Best-Of of match {}".format(yamlParser.ymlDict['match'][0]))
                rootdir = yamlParser.ymlDict['brute_data'] + "{}/".format(yamlParser.ymlDict['match'][0])
                pathData = yamlParser.ymlDict['serialized_path'] + yamlParser.ymlDict['match'][0] + "BOData"
                dirList : list[str] = list()
                for subdir, dirs, _ in os.walk(rootdir):
                    dirList.append(dirs)
                nbGameBo = len(dirList[0])
                gameList = dirList[0]
                allSeparatedData : list[SeparatedData] = []
                allSummaryData : list[SummaryData] = []
                allSnapshot15 : list[Snapshot] = []
                allGameStat15 : list[GameStat] = []

                for i in range(len(yamlParser.ymlDict['match'])):
                    subRootdir = yamlParser.ymlDict['brute_data'] + "/{}/{}".format(yamlParser.ymlDict['match'][i])
                    pathData = yamlParser.ymlDict['brute_data'] + yamlParser.ymlDict['match'][i] + "data"

                    summaryDataTemp : SummaryData = getSummaryData(subRootdir)
                    
                    (separatedDataTemp, gameDuration, begGameTime, endGameTime) = getData(load, yamlParser, idx=i)

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
                print("Computing overview at {} for match {}".format(time, yamlParser.ymlDict['match'][0]))
                (data, gameDuration, begGameTime, endGameTime) = getData(load, yamlParser, idx=0)
                if time != None:
                    snapShot : Snapshot = data.getSnapShotByTime(time, gameDuration)
                    gameStat : GameStat = GameStat(snapShot, gameDuration, begGameTime, endGameTime)
                    path = "{}/GameStat/Overview/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
                    saveDiffStatGame(gameStat, path, snapShot)
                else:
                    snapShot : Snapshot = data.getSnapShotByTime(gameDuration, gameDuration)
                    gameStat : GameStat = GameStat(snapShot, gameDuration, begGameTime, endGameTime)
                    path = "{}/GameStat/OverView/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
                    saveDiffStatGame(gameStat, path, snapShot)
    
    elif jungleProximity:
        print("Getting jungle proximity of game {}".format(yamlParser.ymlDict['match'][0]))
        (data, gameDuration, begGameTime, endGameTime) = getData(load, yamlParser, idx=0)

        splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
        if splitList[-1] > gameDuration:
            splitList[-1] = gameDuration
        else:
            splitList.append(gameDuration)
        splittedDataset : list[SeparatedData] = data.splitData(gameDuration, splitList)
        
        teamNames = data.getTeamNames()

        jungleProxList : list = list()
        for splitData in splittedDataset:
            jungleProxList.append(getJungleProximity(splitData, teamNames['T1']))
        
        print(jungleProxList)

    elif download:
        if dateBeg != None and dateEnd != None:
            assert gameType in GAME_TYPES
            # get_games_by_date(dateBeg, dateEnd, )
        else:
            assert dateBeg == None and dateEnd == None
            assert gameType in GAME_TYPES

            assert number != -1

            print("amount of pages to get : {}".format(number//10))
            nbPage = number//10
            for page in range(nbPage):
                downloadGames(page + fromPage, gameType, yamlParser, load)

    elif draft:
        assert querry != None
        getPlayerPicks(querry, "13.19.535.4316", yamlParser)