from utils_stuff.Position import Position
from Separated.Item import Item
from Separated.Stat import Stat

class Player:
    def __init__(self,
                 championName : str,
                 summonerName : str,
                 participantID : int,
                 level : int,
                 experience : int,
                 attackDamage : int,
                 attackSpeed : int,
                 alive : bool,
                 health : int,
                 healthRegen : int,
                 magicResist : int,
                 armor : int,
                 armorPenetration : int,
                 abilityPower : int,
                 currentGold : int,
                 totalGold : int,
                 position : Position,
                 items : list[Item],
                 stats : Stat) -> None:
        self.championName = championName
        self.summonerName = summonerName
        self.participantID = participantID
        self.level = level
        self.experience = experience
        self.attackDamage = attackDamage
        self.attackSpeed = attackSpeed
        self.alive = alive
        self.health = health
        self.healtRegen = healthRegen
        self.magicResist = magicResist
        self.armor = armor
        self.armorPenetration = armorPenetration
        self.abilityPower = abilityPower
        self.currentGold = currentGold
        self.totalGold = totalGold
        self.position = position
        self.items = items
        self.stats = stats
    
    def getPosition(self):
        return self.position
    
    def CSdiff(self, player):
        return self.stats.minionsKilled - player.stats.minionsKilled

    def goldDiff(self, player):
        return self.totalGold - player.totalGold
    
    def XPdiff(self, player):
        return self.experience - player.experience

    def isAlive(self) -> bool:
        return self.alive