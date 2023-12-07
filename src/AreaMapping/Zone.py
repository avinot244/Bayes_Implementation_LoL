from utils_stuff.Position import Position
from utils_stuff.Computation.Linear import Linear
from utils_stuff.Computation.computation import paralel, getCross

from matplotlib.path import Path

class Zone:
    def __init__(self,
                 boundary : list[Position]) -> None:
        
        # Getting all linear curve between the boundary points
        linearList : list[Linear] = list()
        for i in range(len(boundary[:-1])):
            linearList.append(Linear(coo1=boundary[i], coo2=boundary[i+1]))
        linearList.append(Linear(coo1=boundary[0], coo2=boundary[-1]))
        
        # Checking if the boundary is closing
        i = 0
        res = paralel(linearList[0], linearList[1])
        while (i < len(linearList) - 1 and not(res)):
            res += paralel(linearList[i], linearList[i+1])
            i += 1
        assert i == len(linearList) - 1 
        self.boundary = boundary
    
    def containsPoint(self, coo : Position):
        shape = []
        for pos in self.boundary:
            shape.append(pos.toList())
        bbPath = Path(shape)
        return bbPath.contains_point((coo.x, coo.y))