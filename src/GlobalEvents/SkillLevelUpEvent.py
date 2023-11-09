from utils_stuff.Types import *

class SkillLevelUpEvent:
    def __init__(self,
                 levelUpType : LevelUpType,
                 participantId : int,
                 skillSlot : int,
                 timeStamp : int) -> None:
        self.levelUpType = levelUpType
        self.participantId = participantId
        self.skillSlot = skillSlot
        self.timeStamp = timeStamp