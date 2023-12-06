from AreaMapping.Zone import Zone
from utils_stuff.Position import Position
from utils_stuff.plotsZone import *
from utils_stuff.globals import *
from utils_stuff.Computation.computation import centralSymmetry
import os

midLaneZone = Zone(midLaneBoundary)
topLaneZone = Zone(topLaneBoundary)
botLaneBoundary = [centralSymmetry(coo, mapCenter) for coo in topLaneBoundary]
botLaneZone = Zone(botLaneBoundary)
zoneLst = [midLaneZone, topLaneZone, botLaneZone]
plotZones(zoneLst)