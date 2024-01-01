from YamlParser import YamlParser
from Separated.Game.Snapshot import Snapshot
from GameStat import GameStat
from Separated.Game.SeparatedData import SeparatedData
from EMH.Summary.SummaryData import SummaryData

from utils_stuff.utils_func import getData, getSummaryData
from utils_stuff.stats import plotDiffStatGame, saveDiffStatBO, saveDiffStatGame, stackPlotDiffStatGame


import os


def plotOverView(yamlParser : YamlParser,
                 time : int):
    
    (data, gameDuration , begGameTime, endGameTime) = getData(yamlParser, idx=0)
    snapShot : Snapshot = data.getSnapShotByTime(time, gameDuration)
    gameStat : GameStat = GameStat(snapShot, gameDuration, begGameTime, endGameTime)
    path = "{}/GameStat/Overview/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])

    plotDiffStatGame(gameStat, path, snapShot)

def stackPlotOverview(yamlParser : YamlParser,
                      time : int):
    (data, gameDuration, begGameTime, endGameTime) = getData(yamlParser, idx=0)

    gameStatList : list[GameStat] = list()
    for snapshot in data.gameSnapshotList:
        gameStatList.append(GameStat(snapshot, gameDuration, begGameTime, endGameTime))
    path = "{}/GameStat/Overview/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
    stackPlotDiffStatGame(gameStatList, path, data, time)

def computeOverViewBO(yamlParser : YamlParser,
                      time : int):
    
    rootdir = yamlParser.ymlDict['brute_data'] + "{}/".format(yamlParser.ymlDict['match'][0])
    dirList : list[str] = list()

    for _, dirs, _ in os.walk(rootdir):
        dirList.append(dirs)
    
    allSeparatedData : list[SeparatedData] = []
    allSummaryData : list[SummaryData] = []
    allSnapshot15 : list[Snapshot] = []
    allGameStat15 : list[GameStat] = []

    for i in range(len(yamlParser.ymlDict['match'])):
        subRootdir = yamlParser.ymlDict['brute_data'] + "/{}/{}".format(yamlParser.ymlDict['match'][i])

        summaryDataTemp : SummaryData = getSummaryData(subRootdir)
        
        (separatedDataTemp, gameDuration, begGameTime, endGameTime) = getData(yamlParser, idx=i)

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

def computeOverViewGame(yamlParser : YamlParser,
                        time : int):
    (data, gameDuration, begGameTime, endGameTime) = getData(yamlParser, idx=0)
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