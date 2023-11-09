from utils_stuff.Types import *
from utils_stuff.Position import Position

class BuildingKillEvent: 
    def __init__(self, 
                 bounty : int,
                 building : int,
                 killerid : int,
                 laneType : LaneType,
                 position : Position,
                 teamId : int,
                 timeStamp : int,
                 towerType : TowerType): 
        self.bounty = bounty
        self.building = building
        self.killerid = killerid
        self.laneType = laneType
        self.position = position
        self.teamId = teamId
        self.timeStamp = timeStamp
        self.towerType = towerType