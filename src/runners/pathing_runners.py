from YamlParser import YamlParser
from EMH.Summary.SummaryData import SummaryData
from Separated.Game.SeparatedData import SeparatedData
from utils_stuff.utils_func import getSummaryData, getData, splitPlayerNameListPerTeam
from utils_stuff.plots.plotsTeam import plotBothTeamsPositionAnimated, plotTeamPosition
from utils_stuff.plots.densityPlot import densityPlot, getPositionsMultipleGames, getPositionsSingleGame
from errorHandling import checkTeamComposition
import os

from tqdm import tqdm

def getDataPathing(yamlParser : YamlParser):
    # Loading data of the game
    print("Loading game(s) data")
    
    if len(yamlParser.ymlDict['match']) == 1:
        match = yamlParser.ymlDict['match'][0]
        rootdir = yamlParser.ymlDict['brute_data'] + "{}".format(match)
        # Getting global info of the game
        summaryData : SummaryData = getSummaryData(rootdir)
        (tempData, gameDuration, _, _) = getData(yamlParser, idx=0)

        splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
        if splitList[-1] > gameDuration:
            splitList[-1] = gameDuration
        else:
            splitList.append(gameDuration)
        
        splittedDataset : list[SeparatedData] = tempData.splitData(summaryData.gameDuration, splitList)

        playerNameList = yamlParser.ymlDict['players']

        # TODO : assert if player names in the list are in the game

        return splittedDataset, splitList, playerNameList
    else:
        print("multiple games")
        i = 0
        data : list[list[SeparatedData]] = list()
        for matchName in tqdm(yamlParser.ymlDict['match']):
            rootdir = yamlParser.ymlDict['brute_data'] + matchName

            summaryData : SummaryData = getSummaryData(rootdir)
            (tempData, gameDuration, _, _) = getData(yamlParser, idx=i)
            splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
            if splitList[-1] > gameDuration:
                splitList[-1] = gameDuration
            else:
                splitList.append(gameDuration)
            splittedDataset : list[SeparatedData] = tempData.splitData(summaryData.gameDuration, splitList)

            playerNameList = yamlParser.ymlDict['players']

            # TODO : assert if player names in the list are in the game

            data.append(splittedDataset)
            i += 1
        
        return data, splitList, playerNameList
        


def makeAnimation(yamlParser : YamlParser, 
                  playerNameList : list[str], 
                  splittedDataset : list[SeparatedData], 
                  splitList : list[int]):
    
    if len(yamlParser.ymlDict['match']) == 1:
        print("Ploting pathing with animation of game {} for players {}".format(yamlParser.ymlDict['match'][0], playerNameList))
        if not(os.path.exists("{}/Position/PositionAnimated/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))):
            os.makedirs("{}/Position/PositionAnimated/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))

        i = 0
        for split in splittedDataset:
            name = ""
            if i < len(splitList):
                name = "position_both_teams_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                path = "{}/Position/PositionAnimated/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
                print("saving it to :", path)
                plotBothTeamsPositionAnimated(playerNameList[0], playerNameList[1], split, name, path)        
            i += 1


def makeDensityPlot(yamlParser : YamlParser, 
                    playerNameList : list[str], 
                    data, 
                    splitList : list[int]):
    if len(yamlParser.ymlDict['match']) == 1:

        print("Plotting position density of game {} for players {}".format(yamlParser.ymlDict['match'][0], playerNameList))
        if not(os.path.exists("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))):
            os.makedirs("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))
        save_path = "{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
        
        playerNameList = splitPlayerNameListPerTeam(data[0], playerNameList)
        
        i = 0
        for split in data:
            graph_name = ""
            if i < len(splitList):
                # For team one
                if playerNameList[0]:
                    graph_name = "position_density_teamOne_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                    participantPositions = getPositionsSingleGame(playerNameList[0], split)
                    densityPlot(participantPositions, graph_name, save_path)

                # For team two
                if playerNameList[1]:
                    graph_name = "position_density_teamTwo_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                    participantPositions = getPositionsSingleGame(playerNameList[1], split)
                    densityPlot(participantPositions, graph_name, save_path)
            i += 1
    
    if len(yamlParser.ymlDict['match']) > 1:

        print("Plotting position density of games {} for players {}".format(yamlParser.ymlDict['match'], playerNameList))
        if not(os.path.exists("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))):
            os.makedirs("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))
        save_path = "{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])

        for i in range(len(splitList)):
            # Formating the name of our plot
            nameListStr = ""
            for name in playerNameList:
                nameListStr += "_{}".format(name)
            graph_name = "position_density_{}{}".format(splitList[i], nameListStr)

            # Getting the data of all games for the according split and putting it into a single list
            tempData : list[SeparatedData] = list()
            for game in data:
                if i < len(game):
                    tempData.append(game[i])
            participantPositions = getPositionsMultipleGames(playerNameList, tempData)
            densityPlot(participantPositions, graph_name, save_path)

def makeStaticPlot(yamlParser : YamlParser,
                   playerNameList : list[str],
                   splittedDataset : list[SeparatedData],
                   splitList : list[int]):
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