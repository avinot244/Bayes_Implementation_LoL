from utils_stuff.Types import *

class WardKillEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "killerId":
                self.killerId = v
            elif k == "timestamp":
                self.timestamp = v
            elif k == "wardType":
                self.wardType = v