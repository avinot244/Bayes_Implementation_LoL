class Position:
    def __init__(self,
                 x: int = 0,
                 y: int = 0):
        self.x = x
        self.y = y
    def getPositionFromRawDict(self, rawDict):
        for key, value in rawDict.items():
            if key == "x":
                self.x = value
            elif key == "y":
                self.y = value
    def __str__(self) -> str:
        return "(x: {}, y: {})".format(self.x, self.y)