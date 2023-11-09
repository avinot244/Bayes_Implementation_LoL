from utils_stuff.Types import *
from utils_stuff.Position import Position

class EliteMonsterKillEvent:
    def __init__(self,
                 assistingParticipantsIds : list,
                 bounty : int,
                 killerTeamId : int,
                 monsterSubType : MonsterSubType,
                 monsterType : MonsterType,
                 timeStamp : int,
                 position : Position) -> None:
        self.assistingParticipantsIds = assistingParticipantsIds
        self.bounty = bounty
        self.killerTeamId = killerTeamId
        self.monsterSubType = monsterSubType
        self.monsterType = monsterType
        self.timeStamp = timeStamp
        self.position = position
