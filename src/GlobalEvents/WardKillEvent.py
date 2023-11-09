from utils_stuff.Types import *

class WardKillEvent:
    def __init__(self,
                 killerId : int,
                 timeStamp : int,
                 wardType : WardType) -> None:
        self.killerId = killerId
        self.timeStamp = timeStamp
        self.wardType = wardType