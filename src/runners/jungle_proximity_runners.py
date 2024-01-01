from YamlParser import YamlParser
from Separated.Game.Snapshot import Snapshot
from GameStat import GameStat
from Separated.Game.SeparatedData import SeparatedData
from EMH.Summary.SummaryData import SummaryData

from utils_stuff.utils_func import getData
from utils_stuff.stats import getJungleProximity


def computeJungleProximity(yamlParser : YamlParser):
    (data, gameDuration, begGameTime, endGameTime) = getData(yamlParser, idx=0)

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