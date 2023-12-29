from YamlParser import YamlParser
from Separated.Game.SeparatedData import SeparatedData
import os
import re

def checkMatchName(yamlParser : YamlParser, rootdir : str) -> bool:
    res = True
    for matchName in yamlParser.ymlDict['match']:
        tempres = False
        for _, dir, _ in os.walk(rootdir):
            for file in dir:
                x = re.search(matchName, file)
                if x != None:
                    tempres = True
        res = res and tempres 
    return res

def checkTeamComposition(playerNameList : list[list[str]], data : SeparatedData) -> bool :
    realPlayerList = data.getPlayerList()
    playerTeamOneCheck = True
    playerTeamTwoCheck = True
    for playerName in playerNameList[0]:
        playerTeamOneCheck = playerTeamOneCheck and (playerName in realPlayerList[0])
    
    for playerName in playerNameList[1]:
        playerTeamOneCheck = playerTeamTwoCheck and (playerName in realPlayerList[1])

    return playerTeamOneCheck and playerTeamTwoCheck