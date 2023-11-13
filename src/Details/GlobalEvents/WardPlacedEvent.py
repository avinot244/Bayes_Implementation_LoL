from utils_stuff.Types import *

class WardPlacedEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "creatorId":
                self.creatorId = v
            elif k == "timestamp":
                self.timestamp = v
            elif k == "wardType":
                self.wardType = v