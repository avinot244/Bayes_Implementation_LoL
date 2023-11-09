from utils_stuff.Position import Position
from utils_stuff.Types import *

class TurretPlateDestroyedEvent:
    def __init__(self,
                 killerId : int,
                 laneType : LaneType,
                 position : Position,
                 teamId : int,
                 timeStamp : int) -> None:
        self.killerId = killerId
        self.laneType = laneType
        self.position = position
        self.teamId = teamId
        self.timeStamp = timeStamp