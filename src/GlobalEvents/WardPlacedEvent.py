from utils_stuff.Types import *

class WardPlacedEvent:
    def __init__(self,
                 creatorId : int,
                 timeStamp : int,
                 wardType : WardType) -> None:
        self.creatorId = creatorId
        self.timeStamp = timeStamp
        self.wardType = wardType