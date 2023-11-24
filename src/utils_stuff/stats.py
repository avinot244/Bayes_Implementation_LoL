import csv

from Separated.Snapshot import Snapshot
from Separated.SeparatedData import SeparatedData
from Separated.Player import Player
from utils_stuff.globals import *
from GameStat import GameStat


def saveDiffStatGame(stat : GameStat, game : str, path : str, snapShot : Snapshot):
    teamOneName = snapShot.teamOne.getTeamName()
    teamTwoName = snapShot.teamTwo.getTeamName()

    csv_name = "{}/diff_{}_{}_{}_against_{}.csv".format(path, stat.time, game, teamOneName, teamTwoName)
    csv_name_revert = "{}/diff_{}_{}_{}_against_{}.csv".format(path, stat.time, game, teamTwoName, teamOneName)

    with open(csv_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header =  ["Player_Name", "XPD@{}".format(stat.time), "CSD@{}".format(stat.time), "GD@{}".format(stat.time)]
        writer.writerow(header)
        for i in range(5):
            data = []
            data.append(snapShot.teamOne.players[i].summonerName)
            data.append(stat.playerXPDiff[i])
            data.append(stat.playerCSDiff[i])
            data.append(stat.playerGoldDiff[i])
            writer.writerow(data)
    
    with open(csv_name_revert, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header =  ["Player_Name", "XPD@{}".format(stat.time), "CSD@{}".format(stat.time), "GD@{}".format(stat.time)]
        writer.writerow(header)
        for i in range(5):
            data = []
            data.append(snapShot.teamTwo.players[i].summonerName)
            data.append(-stat.playerXPDiff[i])
            data.append(-stat.playerCSDiff[i])
            data.append(-stat.playerGoldDiff[i])
            writer.writerow(data)          
            
def saveDiffStatBO(statList : list[GameStat], path : str, snapShotList : list[Snapshot]):
    teamOneName = snapShotList[0].teamOne.getTeamName()
    teamTwoName = snapShotList[0].teamTwo.getTeamName()
    timeSaved = statList[0].time

    csv_name = "{}/diff_{}_{}_against_{}.csv".format(path, timeSaved, teamOneName, teamTwoName)
    csv_name_revert = "{}/diff_{}_{}_against_{}.csv".format(path, timeSaved, teamTwoName, teamOneName)
    
    with open(csv_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Player_Name', 'XPD@{}'.format(timeSaved), 'CSD@{}'.format(timeSaved), 'GD@{}'.format(timeSaved)]
        writer.writerow(header)

        playerXPDiffAvg : list[float] = list()
        playerCSDiffAvg : list[float] = list()
        playerGoldDiffAvg : list[float] = list()

        for i in range(5):
            XPDiffAvg : float = 0
            CSDiffAvg : float = 0
            GoldDiffAvg : float = 0
            for stat in statList:
                XPDiffAvg += stat.playerXPDiff[i]
                CSDiffAvg += stat.playerCSDiff[i]
                GoldDiffAvg += stat.playerGoldDiff[i]
            playerXPDiffAvg.append(XPDiffAvg/len(statList))
            playerCSDiffAvg.append(CSDiffAvg/len(statList))
            playerGoldDiffAvg.append(GoldDiffAvg/len(statList))

            data = []
            data.append(snapShotList[0].teamOne.players[i].summonerName)
            data.append(playerXPDiffAvg[i])
            data.append(playerCSDiffAvg[i])
            data.append(playerGoldDiffAvg[i])
            writer.writerow(data)

    with open(csv_name_revert, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Player_Name', 'XPD@{}'.format(timeSaved), 'CSD@{}'.format(timeSaved), 'GD@{}'.format(timeSaved)]
        writer.writerow(header)
        
        playerXPDiffAvg : list[float] = list()
        playerCSDiffAvg : list[float] = list()
        playerGoldDiffAvg : list[float] = list()
        teamGoldDiffAvg : float = 0

        for i in range(5):
            XPDiffAvg : float = 0
            CSDiffAvg : float = 0
            GoldDiffAvg : float = 0
            for stat in statList:
                XPDiffAvg += stat.playerXPDiff[i]
                CSDiffAvg += stat.playerCSDiff[i]
                GoldDiffAvg += stat.playerGoldDiff[i]
            playerXPDiffAvg.append(XPDiffAvg/len(statList))
            playerCSDiffAvg.append(CSDiffAvg/len(statList))
            playerGoldDiffAvg.append(GoldDiffAvg/len(statList))

            data = []
            data.append(snapShotList[0].teamTwo.players[i].summonerName)
            data.append(-playerXPDiffAvg[i])
            data.append(-playerCSDiffAvg[i])
            data.append(-playerGoldDiffAvg[i])
            writer.writerow(data)
        
        
        for stat in statList:
            teamGoldDiffAvg += stat.teamGoldDiff
        teamGoldDiffAvg /= len(statList)
            
            
def getJungleProximity(data : SeparatedData, team : int):
    """team attribute stands for the number of the team (can be either one or two)"""
    jungleProximitySummary : dict = dict()
    
    if team == 0:
        playerList = data.gameSnapshotList[0].teamOne.getPlayerList()
        for playerName in playerList:
            jungleProximitySummary[playerName] = 0
    elif team == 1:
        playerList = data.gameSnapshotList[0].teamTwo.getPlayerList()
        for playerName in playerList:
            jungleProximitySummary[playerName] = 0
    c = 0
    for snapshot in data.gameSnapshotList:
        if team == 0:
            closestPlayer : Player = snapshot.teamOne.getClosesPlayerToJungler()
            jungleProximitySummary[closestPlayer.summonerName] += 1
        elif team == 1:
            closestPlayer : Player = snapshot.teamTwo.getClosesPlayerToJungler()
            jungleProximitySummary[closestPlayer.summonerName] += 1
        c += 1
    
    for k in jungleProximitySummary.keys():
        jungleProximitySummary[k] /= c
    
    return jungleProximitySummary
        


