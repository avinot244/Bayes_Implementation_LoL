from utils_stuff.Position import Position
from PlayerSnapshot.ChampionStats import ChampionStats
from PlayerSnapshot.DamageStats import DamageStats

class PlayerSnaphotClass :
    def __init__(self,
                 participantId : int,
                 championStats : ChampionStats,
                 currentGold : int,
                 damageStats : DamageStats,
                 goldPerSecond : int,
                 jungleMinionsKilled : int,
                 level : int,
                 minionsKilled : int,
                 participandId : int,
                 position : Position,
                 timeEnemySpentControlled : int,
                 totalGold : int,
                 xp : int) -> None:
        self.participandId = participantId
        self.championStats = championStats
        self.currentGold = currentGold
        self.damageStats = damageStats
        self.goldPerSecond = goldPerSecond
        self.jungleMinionsKilled = jungleMinionsKilled
        self.level = level
        self.minionsKilled = minionsKilled
        self.participandId = participandId
        self.position = position
        self.timeEnemySpentControlled = timeEnemySpentControlled
        self.totalGold = totalGold
        self.xp = xp

    def getAtrributeFromRowJson(self, rowJson):
        print(rowJson)
        
    