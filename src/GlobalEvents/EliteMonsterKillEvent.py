from utils_stuff.Types import *
from utils_stuff.Position import Position

class EliteMonsterKillEvent:
    def __init__(self, rawDict : dict) -> None:
        
        for k, v in rawDict.items():
            if k == "assistingParticipantsIds":
                self.assistingParticipantsIds = v
            elif k == "bounty":
                self.bounty = v
            elif k == "killerId":
                self.killerId = v
            elif k == "killerTeamId":
                self.killerTeamId = v
            elif k == "monsterSubType":
                self.monsterSubType = v
            elif k == "monsterType":
                self.monsterType = v
            elif k == "position":
                self.position : Position = Position()
                self.position.getPositionFromRawDict(v)
            elif k == "timestamp":
                self.timestamp = v

