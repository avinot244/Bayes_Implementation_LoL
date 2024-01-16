from AreaMapping.AreaMapping import AreaMapping
from GameStat import GameStat
from Separated.Game.SeparatedData import SeparatedData
from Separated.Game.Snapshot import Snapshot
from Separated.Game.Stat import Stat
from utils_stuff.stats import getJungleProximity
from utils_stuff.globals import roleMap

import csv

def getBehaviorData(areaMapping : AreaMapping, 
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

        if roleMap[participantIdx] == "Top":
            (statDict, lanePresenceMapping) = getBehaviorDataTop(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        elif roleMap[participantIdx] == "Jungle":
            (statDict, lanePresenceMapping) = getBehaviorDataJungle(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        elif roleMap[participantIdx] == "Mid":
            (statDict, lanePresenceMapping) = getBehaviorDataMid(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        elif roleMap[participantIdx] == "ADC":
            (statDict, lanePresenceMapping) = getBehaviorDataADC(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        elif roleMap[participantIdx] == "Support":
            (statDict, lanePresenceMapping) = getBehaviorDataSupport(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        
        return statDict, lanePresenceMapping

    elif datasetSplit.gameSnapshotList[0].teamTwo.isPlayerInTeam(participantID):
        participantIdx : int = datasetSplit.gameSnapshotList[0].teamTwo.getPlayerIdx(participantID)

        if roleMap[participantIdx] == "Top":
            (statDict, lanePresenceMapping) = getBehaviorDataTop(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        elif roleMap[participantIdx] == "Jungle":
            (statDict, lanePresenceMapping) = getBehaviorDataJungle(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        elif roleMap[participantIdx] == "Mid":
            (statDict, lanePresenceMapping) = getBehaviorDataMid(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        elif roleMap[participantIdx] == "ADC":
            (statDict, lanePresenceMapping) = getBehaviorDataADC(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        elif roleMap[participantIdx] == "Support":
            (statDict, lanePresenceMapping) = getBehaviorDataSupport(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        
        return statDict, lanePresenceMapping

def getBehaviorDataTop(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):

    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()
    statDict["XPD@15"] = stat.playerXPDiff[participantIdx]
    statDict["GD@15"] = stat.playerGoldDiff[participantIdx]
    if team == 0:
        statDict["XP/Min"] = 60*snapshot.teamOne.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Gold/Min"] = 60*snapshot.teamOne.players[participantIdx].totalGold/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["CS/Min"] = 60*snapshot.teamOne.players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teamOne.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamOne.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamOne.players[participantIdx].stats.assists

        if snapshot.teamOne.championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teamOne.championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teamOne.players[participantIdx].stats.wardPlaced

        statDict["Damage/Min"] = 60*snapshot.teamOne.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["TotalDamageDealtToBuilding"] = snapshot.teamOne.players[participantIdx].stats.totalDamageDealtToBuildings
        statDict["TotalDamageDealtToObjectives"] = snapshot.teamOne.players[participantIdx].stats.totalDamageDealtToObjectives

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamOneMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamOneMapping[summonerName]["riverTopPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 0)[summonerName]
        
    
    if team == 1 : 
        statDict["XP/Min"] = 60*snapshot.teamTwo.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Gold/Min"] = 60*snapshot.teamTwo.players[participantIdx].totalGold/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["CS/Min"] = 60*snapshot.teamTwo.players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teamTwo.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamTwo.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamTwo.players[participantIdx].stats.assists
        if snapshot.teamTwo.championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teamTwo.championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teamTwo.players[participantIdx].stats.wardPlaced

        statDict["Damage/Min"] = 60*snapshot.teamTwo.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["TotalDamageDealtToBuilding"] = snapshot.teamTwo.players[participantIdx].stats.totalDamageDealtToBuildings
        statDict["TotalDamageDealtToObjectives"] = snapshot.teamTwo.players[participantIdx].stats.totalDamageDealtToObjectives

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamTwoMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamTwoMapping[summonerName]["riverTopPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 1)[summonerName]
    return statDict, lanePresenceMapping
def getBehaviorDataJungle(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):
    
    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()
    statDict["XPD@15"] = stat.playerXPDiff[participantIdx]
    statDict["GD@15"] = stat.playerGoldDiff[participantIdx]
    if team == 0:
        statDict["XP/Min"] = 60*snapshot.teamOne.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Gold/Min"] = 60*snapshot.teamOne.players[participantIdx].totalGold/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teamOne.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamOne.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamOne.players[participantIdx].stats.assists
        if snapshot.teamOne.championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teamOne.championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teamOne.players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teamOne.players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teamOne.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamOneMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamOneMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamOneMapping[summonerName]["botLanePresence"]
        
        lanePresenceMapping["jungleAllyEntryPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyEntryPresence"]
        lanePresenceMapping["jungleEnemyEntryPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyEntryPresence"]
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyBotPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyBotPresence"]

        lanePresenceMapping["riverBotPresence"] = areaMapping.teamOneMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamOneMapping[summonerName]["riverTopPresence"]

    if team == 1 : 
        statDict["XP/Min"] = 60*snapshot.teamTwo.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Gold/Min"] = 60*snapshot.teamTwo.players[participantIdx].totalGold/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teamTwo.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamTwo.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamTwo.players[participantIdx].stats.assists
        if snapshot.teamTwo.championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teamTwo.championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teamTwo.players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teamTwo.players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teamTwo.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

    
        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamTwoMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamTwoMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamTwoMapping[summonerName]["botLanePresence"]
        lanePresenceMapping["jungleAllyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyEntryPresence"]
        lanePresenceMapping["jungleEnemyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyEntryPresence"]

        lanePresenceMapping["jungleAllyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyEntryPresence"]
        lanePresenceMapping["jungleEnemyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyEntryPresence"]
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyBotPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyBotPresence"]

        lanePresenceMapping["riverBotPresence"] = areaMapping.teamTwoMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamTwoMapping[summonerName]["riverTopPresence"]
    
    return statDict, lanePresenceMapping
def getBehaviorDataMid(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):
    
    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()
    statDict["XPD@15"] = stat.playerXPDiff[participantIdx]
    statDict["GD@15"] = stat.playerGoldDiff[participantIdx]
    if team == 0:
        statDict["XP/Min"] = 60*snapshot.teamOne.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Gold/Min"] = 60*snapshot.teamOne.players[participantIdx].totalGold/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["CS/Min"] = 60*snapshot.teamOne.players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teamOne.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamOne.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamOne.players[participantIdx].stats.assists
        if snapshot.teamOne.championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teamOne.championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teamOne.players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teamOne.players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teamOne.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["TotalDamageDealtToBuilding"] = snapshot.teamOne.players[participantIdx].stats.totalDamageDealtToBuildings
        statDict["TotalDamageDealtToObjectives"] = snapshot.teamOne.players[participantIdx].stats.totalDamageDealtToObjectives

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamOneMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamOneMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamOneMapping[summonerName]["botLanePresence"]
        lanePresenceMapping["jungleAllyEntryPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyEntryPresence"]
        lanePresenceMapping["jungleEnemyEntryPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyEntryPresence"]
        
        lanePresenceMapping["riverBotPresence"] = areaMapping.teamOneMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamOneMapping[summonerName]["riverTopPresence"]

        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 0)[summonerName]
    if team == 1 : 
        statDict["XP/Min"] = 60*snapshot.teamTwo.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Gold/Min"] = 60*snapshot.teamTwo.players[participantIdx].totalGold/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["CS/Min"] = 60*snapshot.teamTwo.players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teamTwo.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamTwo.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamTwo.players[participantIdx].stats.assists
        
        if snapshot.teamTwo.championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teamTwo.championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teamTwo.players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teamTwo.players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teamTwo.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["TotalDamageDealtToBuilding"] = snapshot.teamTwo.players[participantIdx].stats.totalDamageDealtToBuildings
        statDict["TotalDamageDealtToObjectives"] = snapshot.teamTwo.players[participantIdx].stats.totalDamageDealtToObjectives

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamTwoMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamTwoMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamTwoMapping[summonerName]["botLanePresence"]
        lanePresenceMapping["jungleAllyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyEntryPresence"]
        lanePresenceMapping["jungleEnemyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyEntryPresence"]
        
        lanePresenceMapping["riverBotPresence"] = areaMapping.teamTwoMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamTwoMapping[summonerName]["riverTopPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 1)[summonerName]
    
    
    return statDict, lanePresenceMapping
def getBehaviorDataADC(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):
    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()
    statDict["XPD@15"] = stat.playerXPDiff[participantIdx]
    statDict["GD@15"] = stat.playerGoldDiff[participantIdx]
    if team == 0:
        statDict["XP/Min"] = 60*snapshot.teamOne.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Gold/Min"] = 60*snapshot.teamOne.players[participantIdx].totalGold/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["CS/Min"] = 60*snapshot.teamOne.players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teamOne.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamOne.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamOne.players[participantIdx].stats.assists
        if snapshot.teamOne.championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teamOne.championKills 
        else :
            statDict["KP%"] = 0


        statDict["Damage/Min"] = 60*snapshot.teamOne.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["botLanePresence"] = areaMapping.teamOneMapping[summonerName]["botLanePresence"]
        
        lanePresenceMapping["riverBotPresence"] =  areaMapping.teamOneMapping[summonerName]["riverBotPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 0)[summonerName]
    if team == 1 : 
        statDict["XP/Min"] = 60*snapshot.teamTwo.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Gold/Min"] = 60*snapshot.teamTwo.players[participantIdx].totalGold/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["CS/Min"] = 60*snapshot.teamTwo.players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teamTwo.players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teamTwo.players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teamTwo.players[participantIdx].stats.assists
        
        if snapshot.teamTwo.championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teamTwo.championKills 
        else :
            statDict["KP%"] = 0


        statDict["Damage/Min"] = 60*snapshot.teamTwo.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["botLanePresence"] = areaMapping.teamTwoMapping[summonerName]["botLanePresence"]
        
        lanePresenceMapping["riverBotPresence"] =  areaMapping.teamTwoMapping[summonerName]["riverBotPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 1)[summonerName]
    
    return statDict, lanePresenceMapping
def getBehaviorDataSupport(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):
    
    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()
    statDict["XPD@15"] = stat.playerXPDiff[participantIdx]
    statDict["GD@15"] = stat.playerGoldDiff[participantIdx]
    if team == 0:
        statDict["XP/Min"] = 60*snapshot.teamOne.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Deaths"] = snapshot.teamOne.players[participantIdx].stats.numDeaths

        if snapshot.teamOne.championKills > 0 :
            statDict["KP%"] = (snapshot.teamOne.players[participantIdx].stats.assists + snapshot.teamOne.players[participantIdx].stats.championsKilled)/snapshot.teamOne.championKills
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teamOne.players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teamOne.players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teamOne.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamOneMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamOneMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamOneMapping[summonerName]["botLanePresence"]
        lanePresenceMapping["jungleAllyEntryPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyEntryPresence"]
        lanePresenceMapping["jungleEnemyEntryPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyEntryPresence"]
        
        lanePresenceMapping["jungleAllyEntryPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyEntryPresence"]
        lanePresenceMapping["jungleEnemyEntryPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyEntryPresence"]
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyBotPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyBotPresence"]

        lanePresenceMapping["riverBotPresence"] = areaMapping.teamOneMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamOneMapping[summonerName]["riverTopPresence"]

        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 0)[summonerName]
    if team == 1 : 
        statDict["XP/Min"] = 60*snapshot.teamTwo.players[participantIdx].experience/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Deaths"] = snapshot.teamTwo.players[participantIdx].stats.numDeaths
        
        if snapshot.teamTwo.championKills > 0 :
            statDict["KP%"] = (snapshot.teamTwo.players[participantIdx].stats.assists + snapshot.teamTwo.players[participantIdx].stats.championsKilled)/snapshot.teamTwo.championKills
        else :
            statDict["KP%"] = 0
        
        statDict["WardPlaced"] = snapshot.teamTwo.players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teamTwo.players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teamTwo.players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamTwoMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamTwoMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamTwoMapping[summonerName]["botLanePresence"]
        lanePresenceMapping["jungleAllyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyEntryPresence"]
        lanePresenceMapping["jungleEnemyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyEntryPresence"]
        
        lanePresenceMapping["jungleAllyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyEntryPresence"]
        lanePresenceMapping["jungleEnemyEntryPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyEntryPresence"]
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyBotPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyBotPresence"]

        lanePresenceMapping["riverBotPresence"] = areaMapping.teamTwoMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamTwoMapping[summonerName]["riverTopPresence"]
    
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 1)[summonerName]
    
    
    return statDict, lanePresenceMapping

def saveToDataBase(statDict : dict, 
                   lanePresenceMapping : dict,
                   path : str,
                   new : bool,
                   matchId : str,
                   summonnerName : str,
                   role : str):
    
    # Asserting the right open option
    if new:
        open_option = 'w'
    else:
        open_option = 'a'
    
    full_path = path + "behavior_{}.csv".format(role)
    with open(full_path, open_option) as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        if new :
            header = ["MatchId", "SummonnerName"]
            for key in statDict.keys():
                header.append(key)
            for key in lanePresenceMapping.keys():
                header.append(key)
            writer.writerow(header)
        
        data : list = list()
        data.append(matchId)
        data.append(summonnerName)
        for _, v in statDict.items():
            data.append(v)
        for _, v in lanePresenceMapping.items():
            data.append(v)
        
        writer.writerow(data)
