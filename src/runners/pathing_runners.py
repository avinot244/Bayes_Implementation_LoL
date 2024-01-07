from YamlParser import YamlParser
from EMH.Summary.SummaryData import SummaryData
from Separated.Game.SeparatedData import SeparatedData
from utils_stuff.utils_func import getSummaryData, getData
from utils_stuff.plots.plotsTeam import plotBothTeamsPositionAnimated, plotTeamPosition
from utils_stuff.plots.densityPlot import densityPlot, getPositionsMultipleGames, getPositionsSingleGame
from errorHandling import checkTeamComposition
import os

def getDataPathing(yamlParser : YamlParser):
    # Loading data of the game
    
    if len(yamlParser.ymlDict['match']) == 1:
        match = yamlParser.ymlDict['match'][0]
        rootdir = yamlParser.ymlDict['brute_data'] + "{}".format(match)
        # Getting global info of the game
        summaryData : SummaryData = getSummaryData(rootdir)
        (data, gameDuration, _, _) = getData(yamlParser, idx=0)

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

        return splittedDataset, splitList, playerNameList
    else:
        print("multiple games")
        i = 0
        data : list[list[SeparatedData]] = list()
        for match in yamlParser.ymlDict['match']:
            rootdir = yamlParser.ymlDict['brute_data'] + match

            summaryData : SummaryData = getSummaryData(rootdir)
            (data, gameDuration, _, _) = getData(yamlParser, idx=i)
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
        
        i = 0
        for split in data:
            graph_name = ""
            if i < len(splitList):
                # For team one
                graph_name = "position_density_teamOne_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                participantPositions = getPositionsSingleGame(playerNameList[0], split)
                densityPlot(participantPositions, graph_name, save_path)

                # For team two
                graph_name = "position_density_teamTwo_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                participantPositions = getPositionsSingleGame(playerNameList[1], split)
                densityPlot(participantPositions, graph_name, save_path)
            i += 1
    
    if len(yamlParser.ymlDict['match']) > 1:
        print("Plotting position density of games {} for players {}".format(yamlParser.ymlDict['match'], playerNameList))
        if not(os.path.exists("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))):
            os.makedirs("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))
        save_path = "{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])
        
        i = 0
        for separatedDataList in data:
            graph_name = ""
            if i < len(splitList):
                # For team one
                graph_name = "position_density_teamOne_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                participantPositions = getPositionsMultipleGames(playerNameList[0], separatedDataList)
                densityPlot(participantPositions, graph_name, save_path)

                # For team two
                graph_name = "position_density_teamTwo_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
                participantPositions = getPositionsMultipleGames(playerNameList[1], separatedDataList)
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