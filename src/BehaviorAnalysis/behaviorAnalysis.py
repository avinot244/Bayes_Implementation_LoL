from AreaMapping.AreaMapping import AreaMapping
from GameStat import GameStat
from Separated.Game.SeparatedData import SeparatedData
from Separated.Game.Snapshot import Snapshot
from Separated.Game.Stat import Stat
from utils_stuff.stats import getJungleProximity

import csv

def getBehaviorData(areMapping : AreaMapping, 
                    stat : GameStat, 
                    datasetSplit : SeparatedData, 
                    summonerName : str,
                    time : int,
                    gameDuration : int):
    # areaMapping and stat objects must already be computed !
    # datasetSplit must be the right split of the game we want to analyse !
    

    participantID = datasetSplit.getPlayerID(summonerName)
    snapshot : Snapshot = datasetSplit.getSnapShotByTime(time, gameDuration)

    # Getting the team where the player is
    if datasetSplit.gameSnapshotList[0].teamOne.isPlayerInTeam(participantID):
        participantIdx : int = datasetSplit.gameSnapshotList[0].teamOne.getPlayerIdx(participantID)
        
        # Computing general statistics about the player
        statDict : dict = dict()
        statDict["Kills"] = snapshot.teamOne.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamOne.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamOne.players[participantIdx].stats.assists
        statDict["DamageDealt"] = snapshot.teamOne.players[participantIdx].stats.totalDamageDealt
        statDict["DamageTaken"] = snapshot.teamOne.players[participantIdx].stats.totalDamageTaken
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 0)

        lanePresenceMapping = areMapping.teamOneMapping[summonerName]
        csDiff : float = stat.playerCSDiff[participantIdx]
        goldDiff : float = stat.playerGoldDiff[participantIdx]

        return csDiff, goldDiff, statDict, lanePresenceMapping

    elif datasetSplit.gameSnapshotList[0].teamTwo.isPlayerInTeam(participantID) :
        participantIdx : int = datasetSplit.gameSnapshotList[0].teamTwo.getPlayerIdx(participantID)
        
        # Computing general statistics about the player
        statDict : dict = dict()
        statDict["Kills"] = snapshot.teamTwo.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamTwo.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamTwo.players[participantIdx].stats.assists
        statDict["DamageDealt"] = snapshot.teamTwo.players[participantIdx].stats.totalDamageDealt
        statDict["DamageTaken"] = snapshot.teamTwo.players[participantIdx].stats.totalDamageTaken
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 1)[summonerName]

        lanePresenceMapping = areMapping.teamTwoMapping[summonerName]
        csDiff : float = stat.playerCSDiff[participantIdx]
        goldDiff : float = stat.playerGoldDiff[participantIdx]

        return csDiff, goldDiff, statDict, lanePresenceMapping

def saveToDataBase(csDiff : float, 
                   goldDiff : float, 
                   statDict : dict, 
                   lanePresenceMapping : dict,
                   path : str,
                   new : bool,
                   matchId : str,
                   summonnerName : str):
    
    # Asserting the right open option
    if new:
        open_option = 'w'
    else:
        open_option = 'a'
    
    full_path = path + "behavior.csv"
    with open(full_path, open_option) as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        if new :
            header = ["MatchId", "SummonnerName","CSD@15","GD@15"]
            for key in statDict.keys():
                header.append(key)
            for key in lanePresenceMapping.keys():
                header.append(key)
            writer.writerow(header)
        
        data : list = list()
        data.append(matchId)
        data.append(summonnerName)
        data.append(csDiff)
        data.append(goldDiff)
        for _, v in statDict.items():
            data.append(v)
        
        for _, v in lanePresenceMapping.items():
            data.append(v)
        
        writer.writerow(data)