from utils_stuff.Types import *

class SkillLevelUpEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "levelUpType":
                self.levelUpType = v
            elif k == "participantId":
                self.participantId = v
            elif k == "skillSlot":
                self.skillSlot = v
            elif k == "timestamp":
                self.timestamp = v