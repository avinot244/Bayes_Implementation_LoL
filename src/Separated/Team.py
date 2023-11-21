from Separated.Player import Player
from utils_stuff.Position import Position

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
        