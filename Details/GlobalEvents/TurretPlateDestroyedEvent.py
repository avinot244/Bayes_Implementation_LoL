from utils_stuff.Position import Position
from utils_stuff.Types import *

class TurretPlateDestroyedEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "killerId":
                self.killerId = v
            elif k == "laneType":
                self.laneType = v
            elif k == "position":
                self.position : Position = Position()
                self.position.getPositionFromRawDict(v)
            elif k == "teamId":
                self.teamId = v
            elif k == "timestamp":
                self.timestamp = v