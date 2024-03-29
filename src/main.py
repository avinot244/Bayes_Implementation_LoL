# clear && python3 main.py --match NORDvsBRUTE --game 1 --file DETAILS
# clear && python3 main.py --match JDGvsT1 --game 1 --file DETAILS

import argparse
import os

from utils_stuff.globals import *
from utils_stuff.utils_func import getSummaryData, getData, getRole
from utils_stuff.Types import *
from utils_stuff.plots.plotsTeam import *
from utils_stuff.stats import *
from errorHandling import checkMatchName

from EMH.Summary.SummaryData import SummaryData
from Separated.Game.SeparatedData import SeparatedData
from Separated.Game.Snapshot import Snapshot
from GameStat import GameStat
from YamlParser import YamlParser
from draftDBQueries.getPlayerPicks import getPlayerPicks
from AreaMapping.AreaMapping import AreaMapping

from runners.global_runners import downloadGames, areaMappingRunner
from runners.pathing_runners import getDataPathing, makeAnimation, makeDensityPlot, makeStaticPlot
from runners.overview_runners import plotOverView, computeOverViewBO, computeOverViewGame, stackPlotOverview
from runners.jungle_proximity_runners import computeJungleProximity
from BehaviorAnalysis.behaviorAnalysis import getBehaviorData, saveToDataBase

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-p", "--pathing", action="store_true", default=False, help="Tells if we want to print pathing of players")
    parser.add_argument("-a", "--anim", action="store_true", default=False, help="Tells if we want to plot animations. Only with --pathing option")
    parser.add_argument("-d", "--density", action="store_true", default=False, help="Tells if we want to plot the position density. Only with --pathing option")
   
    parser.add_argument("-o", "--overview", action="store_true", default=False, help="Compute game stat of players")
    parser.add_argument("-gr", "--graph", action="store_true", default=False, help="Tells if we want to plot the stats")
    parser.add_argument("-t", "--time", metavar="[time_wanted_in_seconds]", type=int, help="Game time to analyse")
    
    parser.add_argument("-j", "--jungle-prox", action="store_true", default=False, help="Prints jungle proximity at a given time")
    parser.add_argument("-lp", "--lane-presence", action="store_true", default=False, help="Prints jungle presense at a given time")

    parser.add_argument("-dl", "--download", action="store_true", default=False, help="Tells if we want to download game data from api")
    parser.add_argument("-dB", "--dateBeg", metavar="[YYYY-MM-DD]", type=str, help="Beginning date of when we extract game")
    parser.add_argument("-dE", "--dateEnd", metavar="[YYYY-MM-DD]", type=str, help="End date of when we extract game")
    parser.add_argument("-gT", "--game-type", metavar="[ESPORTS, SCRIM, CHAMPIONS_QUEUE, GENERIC]", type=str, help="Game type we want to download")
    parser.add_argument("-dlO", "--download-option", metavar="[GAMH_DETAILS, GAMH_SUMMARY, ROFL_REPLAY, HISTORIC_BAYES_SEPARATED, HISTORIC_BAYES_DUMP]", type=str, help="Type of data we want to downoad form the game")
    parser.add_argument("-n", "--number", metavar="[Amounf_of_game_wanted]", type=int, help="Amount of game we want to download")
    parser.add_argument("-f", "--from", metavar="[page_number]", type=int, help="Page number from where we get data")

    parser.add_argument("-pr", "--pick-rate", metavar="[player_name]", type=str, help="Name of the player we want to get pick rate")
    parser.add_argument("-qr", "--querry", metavar="[player_name]", type=str, help="Gets the pickrate of each champion of the given player")

    parser.add_argument("-b", "--behavior-analysis", action="store_true", default=False, help="Does behavior analysis")

    args = parser.parse_args()
    args_data = vars(args)

    pathing = False
    anim = False
    density = False
    overview = False
    time = 0
    jungleProximity = False
    lanePresence = False
    graph = False
    download = False
    dateBeg, dateEnd = ("", "")
    gameType = ""
    draft = False
    querry = ""
    number = -1
    fromPage = 0
    behaviorAnalysis = False

    for arg, value in args_data.items():
        if arg == "pathing" : pathing = value 
        if arg == "anim" : anim = value
        if arg == "overview" : overview = value
        if arg == "graph" : graph = value
        if arg == "time" : time = value
        if arg == "jungle_prox" : jungleProximity = value
        if arg == "lane_presence": lanePresence = value
        if arg == "density" : density = value
        if arg == "download" : download = value
        if arg == "dateBeg" : dateBeg = value
        if arg == "dateEnd" : dateEnd = value
        if arg == "game_type" : gameType = value
        if arg == "draft" : draft = value
        if arg == "querry" : querry = value
        if arg == "number" : number = value
        if arg == "from" : fromPage = value
        if arg == "behavior_analysis" : behaviorAnalysis = value

    yamlParser : YamlParser = YamlParser("./config.yml")
    if not(download):
        assert checkMatchName(yamlParser, DATA_PATH)

    if pathing:
        (data, splitList, playerNameList) = getDataPathing(yamlParser)
        if anim:
            makeAnimation(yamlParser, playerNameList, data, splitList)
        elif density:
            makeDensityPlot(yamlParser, playerNameList, data, splitList)
        else:
            makeStaticPlot(yamlParser, playerNameList, data, splitList)
            
    elif overview:
        if not(os.path.exists(yamlParser.ymlDict['save_path'] + "/GameStat/OverView/{}/".format(yamlParser.ymlDict['match'][0]))):
            os.makedirs(yamlParser.ymlDict['save_path'] + "/GameStat/OverView/{}/".format(yamlParser.ymlDict['match'][0]))
        if graph:
            if len(yamlParser.ymlDict['match']) > 1:
                print("Plotting overview of the whole Best-Of of match {}".format(yamlParser.ymlDict['match']))
            else:
                assert time != None
                print("Plotting overview at {} for match {}".format(time, yamlParser.ymlDict['match'][0]))
                # plotOverView(yamlParser, load, time)
                print("Plotting GoldDiff evolution before {} for match {}".format(time, yamlParser.ymlDict['match'][0]))
                stackPlotOverview(yamlParser, time)
        else :
            if len(yamlParser.ymlDict['match']) > 1:
                print("Computing overview of the whole Best-Of of match {}".format(yamlParser.ymlDict['match'][0]))
                computeOverViewBO(yamlParser, time)
            
            else:
                print("Computing overview at {} for match {}".format(time, yamlParser.ymlDict['match'][0]))
                computeOverViewGame(yamlParser, time)
    
    elif jungleProximity:
        print("Getting jungle proximity of game {}".format(yamlParser.ymlDict['match'][0]))
        computeJungleProximity(yamlParser)

    elif lanePresence:
        assert time != None
        assert time > 120
        print("Getting lane presence of game {}".format(yamlParser.ymlDict['match'][0]))
        areaMappingRunner(yamlParser, time)

    elif download:
        if dateBeg != None and dateEnd != None:
            assert gameType in GAME_TYPES
            # get_games_by_date(dateBeg, dateEnd, )
        else:
            assert dateBeg == None and dateEnd == None
            assert gameType in GAME_TYPES
            assert number != -1

            print(gameType)
            print("amount of pages to get : {}".format(number//10))
            nbPage = number//10
            for page in range(nbPage):
                downloadGames(page + fromPage, gameType, yamlParser)
    
    elif draft:
        assert querry != None
        getPlayerPicks(querry, "13.19.535.4316", yamlParser)
    
    elif behaviorAnalysis:
        assert time != None
        assert time > 120
        print("Behavior Analysis")
        for i in range(len(yamlParser.ymlDict['match'])):
            (data, gameDuration, begGameTime, endGameTime) = getData(yamlParser, idx=i)
            matchId = data.matchId
            
            # Splitting our data so we get the interval between [950s; time]
            splitList : list[int] = [120, time, gameDuration]
            splittedDataset : list[SeparatedData] = data.splitData(gameDuration, splitList)
            areaMapping : AreaMapping = AreaMapping()

            dataBeforeTime : SeparatedData = splittedDataset[1] # Getting the wanted interval
            areaMapping.computeMapping(dataBeforeTime)

            for playerTeamOne in dataBeforeTime.gameSnapshotList[0].teamOne.players:
                summonnerName = playerTeamOne.summonerName
                role = getRole(dataBeforeTime, summonnerName)

                gameStat : GameStat = GameStat(dataBeforeTime.getSnapShotByTime(time, gameDuration), gameDuration, begGameTime, endGameTime) 

                (statDict, lanePresenceMapping) = getBehaviorData(areaMapping, gameStat, dataBeforeTime, summonnerName, time, gameDuration)

                if not(os.path.exists("{}/behavior/".format(yamlParser.ymlDict['database_path']))):
                    os.mkdir("{}/behavior/".format(yamlParser.ymlDict['database_path']))
                
                new = False
                if not(os.path.exists("{}/behavior/behavior_{}.csv".format(yamlParser.ymlDict['database_path'], role))):
                    new = True
                save_path = "{}/behavior/".format(yamlParser.ymlDict['database_path'])
                
                saveToDataBase(statDict, lanePresenceMapping, save_path, new, matchId, summonnerName, role)
            
            for playerTeamTwo in dataBeforeTime.gameSnapshotList[0].teamTwo.players:
                summonnerName = playerTeamTwo.summonerName
                role = getRole(dataBeforeTime, summonnerName)

                gameStat : GameStat = GameStat(dataBeforeTime.getSnapShotByTime(time, gameDuration), gameDuration, begGameTime, endGameTime) 

                (tatDict, lanePresenceMapping) = getBehaviorData(areaMapping, gameStat, dataBeforeTime, summonnerName, time, gameDuration)
                
                if not(os.path.exists("{}/behavior/".format(yamlParser.ymlDict['database_path']))):
                    os.mkdir("{}/behavior/".format(yamlParser.ymlDict['database_path']))
                
                new = False
                if not(os.path.exists("{}/behavior/behavior_{}.csv".format(yamlParser.ymlDict['database_path'], role))):
                    new = True
                save_path = "{}/behavior/".format(yamlParser.ymlDict['database_path'])

                saveToDataBase(statDict, lanePresenceMapping, save_path, new, matchId, summonnerName, role)

