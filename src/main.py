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
from Separated.Game.SeparatedData import SeparatedData
from Separated.Game.Snapshot import Snapshot
from Separated.Game.Player import Player
from GameStat import GameStat
from YamlParser import YamlParer
from API.Bayes.api_calls import get_games_by_date, get_games_by_page, save_downloaded_file, get_download_link
from Separated.Draft.Draft import Draft
from draftDBQueries.getPlayerPicks import getPlayerPicks




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-p", "--pathing", action="store_true", default=False, help="Tells if we want to print pathing of players")
    parser.add_argument("-a", "--anim", action="store_true", default=False, help="Tells if we want to plot animations. Only with --pathing option")
    parser.add_argument("-d", "--density", action="store_true", default=False, help="Tells if we want to plot the position density. Only with --pathing option")
    parser.add_argument("-g", "--game", metavar="[1|2|3|4|5|BO]", type=str, help="Game to analyse or if we want the whole Best-Off")
    
    parser.add_argument("-o", "--overview", action="store_true", default=False, help="Compute game stat of players")
    parser.add_argument("-gr", "--graph", action="store_true", default=False, help="Tells if we want to plot the stats")
    parser.add_argument("-t", "--time", metavar="[time_wanted_in_seconds]", type=int, help="Game time to analyse")
    
    parser.add_argument("-j", "--jungle-prox", action="store_true", default=False, help="Prints jungle proximity at a given time")
    parser.add_argument("-l", "--load", action="store_true", default=False, help="Tells if we want to load serialized object")
    
    parser.add_argument("-dl", "--download", action="store_true", default=False, help="Tells if we want to download game data from api")
    parser.add_argument("-dB", "--dateBeg", metavar="[YYYY-MM-DD]", type=str, help="Beginning date of when we extract game")
    parser.add_argument("-dE", "--dateEnd", metavar="[YYYY-MM-DD]", type=str, help="End date of when we extract game")
    parser.add_argument("-pa", "--page", metavar="[int]", type=int, help="Page of 10 games we want to download")
    parser.add_argument("-gT", "--game-type", metavar="[ESPORTS, SCRIM, CHAMPIONS_QUEUE, GENERIC]", type=str, help="Game type we want to download")
    parser.add_argument("-dlO", "--download-option", metavar="[GAMH_DETAILS, GAMH_SUMMARY, ROFL_REPLAY, HISTORIC_BAYES_SEPARATED, HISTORIC_BAYES_DUMP]", type=str, help="Type of data we want to downoad form the game")

    parser.add_argument("-dr", "--draft", action="store_true", default=False, help="Tells if we want to get draft details")
    parser.add_argument("-pr", "--pick-rate", metavar="[player_name]", type=str, help="Name of the player we want to get pick rate")
    parser.add_argument("-qr", "--querry", metavar="[player_name]", type=str, help="Gets the pickrate of each champion of the given player")

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
    graph = False
    download = False
    dateBeg, dateEnd = ("", "")
    page = -1
    gameType = ""
    downloadOption = ""
    draft = False
    querry = ""

    for arg, value in args_data.items():
        if arg == "pathing":
            pathing = value
        if arg == "anim":
            anim = value
        if arg == "game":
            game = value
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
        if arg == "page":
            page = value
        if arg == "game_type":
            gameType = value
        if arg == "download_option":
            downloadOption = value
        if arg == "draft":
            draft = value
        if arg == "querry":
            querry = value

    yamlParser : YamlParer = YamlParer("./config.yml")
    if not(download):
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
        if graph:
            if game == "BO":
                print("Plotting overview of th whole Best-Of of match {}".format(yamlParser.ymlDict['match']))
            else:
                print("Plotting overview of game {} at {} for match {}".format(game, time, yamlParser.ymlDict['match']))
                (data, gameDuration , begGameTime, endGameTime) = getData(load, yamlParser, game)
                if time != None:
                    snapShot : Snapshot = data.getSnapShotByTime(time, gameDuration)
                    gameStat : GameStat = GameStat(snapShot, gameDuration, begGameTime, endGameTime)
                    path = "{}/GameStat/Overview/{}/g{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'], game)
                    #TODO : do graph stuff

                    plotDiffStatGame(gameStat, "g{}".format(game), path, snapShot)
                    
        else :
            if game == "BO":
                print("Computing overview of the whole Best-Of of match {}".format(yamlParser.ymlDict['match']))
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
                print("Computing overview of game {} at {} for match {}".format(game, time, yamlParser.ymlDict['match']))
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

    elif download:
        if dateBeg != None and dateEnd != None:
            assert page == -1
            assert gameType in GAME_TYPES
            assert downloadOption != None
            # get_games_by_date(dateBeg, dateEnd, )
        elif page != -1:
            assert dateBeg == None and dateEnd == None
            assert gameType in GAME_TYPES
            assert downloadOption != None

            gameNames : list[str] = get_games_by_page(page, gameType)
            for gameName in gameNames :
                if not(os.path.exists(yamlParser.ymlDict['brute_data'] + "{}/g1/Separated/".format(gameName))):
                    os.makedirs(yamlParser.ymlDict['brute_data'] + "{}/g1/Separated/".format(gameName))

                path = yamlParser.ymlDict['brute_data'] + "{}/g1".format(gameName)

                if downloadOption == "HISTORIC_BAYES_SEPARATED":
                    path += "/Separated/"
                
                save_downloaded_file(get_download_link(gameName, downloadOption), path, gameName, downloadOption)
    elif draft:
        if querry == None:
            print("Getting draft of game {}".format(yamlParser.ymlDict['match']))

            # Set upping ath for database saving
            if not(os.path.exists("{}/drafts/".format(yamlParser.ymlDict['database_path']))):
                os.mkdir("{}/drafts/".format(yamlParser.ymlDict['database_path']))
            new = False
            if not(os.path.exists("{}/drafts/draft_pick_order.csv".format(yamlParser.ymlDict['database_path']))):
                new = True
            save_path = "{}/drafts/".format(yamlParser.ymlDict['database_path'])

            # Loading data of the game
            match = yamlParser.ymlDict['match']
            rootdir = yamlParser.ymlDict['brute_data'] + "{}/g{}".format(match, game)
            # Getting global info of the game
            summaryData : SummaryData = getSummaryData(rootdir)
            (data, gameDuration, begGameTime, endGameTime) = getData(load, yamlParser, game)
            patch = summaryData.patch
            data.draftToCSV(save_path, new, patch)
        else:
            getPlayerPicks(querry, "13.19.535.4316", yamlParser)