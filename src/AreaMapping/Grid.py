from AreaMapping.Zone import Zone
from utils_stuff.Position import Position

class Grid:
    def __init__(self,
                 zoneList : list[Zone]) -> None:
        self.zoneList = zoneList

    def containsPoint(self, coo : Position):
        res = False
        for zone in self.zoneList:
            res = res or zone.containsPoint(coo)
        return res