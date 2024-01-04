from YamlParser import YamlParser
from Separated.Game.SeparatedData import SeparatedData
import os
import re

def checkMatchName(yamlParser : YamlParser, rootdir : str) -> bool:
    res = True
    for matchName in yamlParser.ymlDict['match']:
        tempRes = False
        for item in os.listdir(rootdir):
            # print(os.path.join(rootdir, item))
            if os.path.isfile(os.path.join(rootdir, item)):
                if re.search(matchName, os.path.join(rootdir, item)) != None:
                    tempRes = True
            if os.path.isdir(os.path.join(rootdir, item)):
                if re.search(matchName, os.path.join(rootdir, item)) != None:
                    tempRes = True
        
        res = res and tempRes 
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