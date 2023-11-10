from utils_stuff.Types import *
from utils_stuff.Position import Position

class BuildingKillEvent: 
    def __init__(self, rawDict : dict): 
        for k, v in rawDict.items():
            if k == "bounty":
                self.bounty = v
            elif k == "buildingType":
                self.buildingType = v
            elif k == "killerId":
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
            elif k == "towerType":
                self.towerType = v