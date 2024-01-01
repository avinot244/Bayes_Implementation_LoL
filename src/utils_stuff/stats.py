import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

from Separated.Game.Snapshot import Snapshot
from Separated.Game.SeparatedData import SeparatedData
from Separated.Game.Player import Player
from utils_stuff.globals import *
from GameStat import GameStat


def saveDiffStatGame(stat : GameStat, path : str, snapShot : Snapshot):
    teamOneName = snapShot.teamOne.getTeamName()
    teamTwoName = snapShot.teamTwo.getTeamName()

    csv_name = "{}diff_{}_{}_against_{}.csv".format(path, stat.time, teamOneName, teamTwoName)

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
              

def plotDiffStatGame(stat : GameStat, path : str, snapShot : Snapshot):
    saveDiffStatGame(stat, path, snapShot)
    teamOneName = snapShot.teamOne.getTeamName()
    teamTwoName = snapShot.teamTwo.getTeamName()
    csv_name = "{}/diff_{}_{}_against_{}.csv".format(path, stat.time, teamOneName, teamTwoName)
    
    df = pd.read_csv(csv_name)
    labels = ["XPD@{}".format(stat.time), "CSD@{}".format(stat.time), "GD@{}".format(stat.time)]
    idx = 0

    for idx in range(len(df)):
        playerName = df.iloc[idx].to_list()[0]
        data = df.iloc[idx].to_list()[1:]
    
        plt.barh(y=labels, width=data)
        plt.savefig("{}/BarPlot{}.png".format(path, playerName))
        plt.clf()

def stackPlotDiffStatGame(stats : list[GameStat], path : str, snapshots : SeparatedData, time : int):
    goldDiffTeam : list[float] = list()
    goldDiffPlayer : list = [[], [], [], [], []]
    x : list = list()

    for stat in stats:
        if stat.time < time//60:
            
            for i in range(len(stat.playerGoldDiff)):
                goldDiffPlayer[i].append(stat.playerGoldDiff[i])
            goldDiffTeam.append(sum([goldDiffPlayer[j][-1] for j in range(5)]))
            x.append(stat.time)
        
    print(snapshots.getTeamNames())
    print(snapshots.getPlayerList())

    inv_map = {}
    for k, v in snapshots.getTeamNames().items():
        inv_map[v] = inv_map.get(v, []) + [k]
    labels = [inv_map[0][0] + " vs " + inv_map[1][0]]
    for i in range(5):
        labels.append(snapshots.getPlayerList()[0][i] + " vs " + snapshots.getPlayerList()[1][i])
    
    # x = np.arange(0, time//60, len(goldDiffTeam)/(time//60))
    
    plt.fill_between(x, goldDiffTeam, label=labels[0], zorder=-1)
    for i in range(5):
        plt.plot(x, goldDiffPlayer[i], label=labels[i+1])
    
    plt.axhline(0, color="black", ls="--")
    plt.legend(loc='upper left')
    plt.savefig("{}/GoldDiffEvolutionBefore{}min.png".format(path,time//60))
    plt.clf()

def saveDiffStatBO(statList : list[GameStat], path : str, snapShotList : list[Snapshot]):
    teamOneName = snapShotList[0].teamOne.getTeamName()
    teamTwoName = snapShotList[0].teamTwo.getTeamName()
    timeSaved = statList[0].time

    csv_name = "{}/diff_{}_{}_against_{}.csv".format(path, timeSaved, teamOneName, teamTwoName)
    
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
        


