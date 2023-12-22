from Separated.Game.Player import Player
from utils_stuff.Position import Position
from utils_stuff.Computation.computation import abs_dist

import re

class Team:
    def __init__(self,
                 assists : int,
                 baronKills : int,
                 championKills : int,
                 deaths : int,
                 dragonKills : int,
                 teamID : int,
                 inhibKills : int,
                 totalGold : int,
                 towerKills : int,
                 killedDragonTypes : list[str],
                 players : list[Player]) -> None:
        self.assists = assists
        self.baronKills = baronKills
        self.championKills = championKills
        self.deaths = deaths
        self.dragonKills = dragonKills
        self.teamID = teamID
        self.inhibKills = inhibKills
        self.totalGold = totalGold
        self.towerKills = towerKills
        self.killedDragonTypes = killedDragonTypes
        self.players = players
    
    def getPlayerList(self):
        playerList : list[str] = list()
        for player in self.players:
            playerList.append(player.summonerName)
        return playerList
    
    def isPlayerInTeam(self, participantID):
        for player in self.players:
            if player.participantID == participantID:
                return True
        return False
    
    def getPlayerIdx(self, participantID):
        i : int = 0
        for player in self.players:
            if player.participantID == participantID:
                return i
            i += 1

    def getPlayerPosition(self, playerIdx) -> Position:
        return self.players[playerIdx].position
    
    def getPlayerID(self, playerName) -> int:
        for player in self.players:
            if player.summonerName == playerName:
                return player.participantID
    
    def getTeamName(self) -> str:
        splits = re.split("\s", self.players[0].summonerName)
        return splits[0]

    def getClosesPlayerToJungler(self) -> Player:
        jungle = self.players[1]
        dist = abs_dist(jungle.position, self.players[0].position)
        idx = 0
        for i in range(len(self.players)):
            if i != 1:
                distTemp = abs_dist(jungle.position, self.players[i].position)
                if distTemp < dist:
                    dist = distTemp
                    idx = i
        return self.players[idx]