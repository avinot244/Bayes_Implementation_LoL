from Separated.Player import Player

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