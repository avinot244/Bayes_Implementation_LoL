from AreaMapping.Zone import Zone
from utils_stuff.Position import Position
from utils_stuff.plotsZone import *
from utils_stuff.globals import *
from utils_stuff.Computation.computation import centralSymmetry
import os

midLaneZone = Zone(midLaneBoundary)
topLaneZone = Zone(topLaneBoundary)
botLaneZone = Zone(botLaneBoundary)
jungleEntry1BlueZone = Zone(jungleEntry1Blue)
jungleEntry2BlueZone = Zone(jungleEntry2Blue)
jungleEntry3BlueZone = Zone(jungleEntry3Blue)
jungleEntry4BlueZone = Zone(jungleEntry4Blue)

jungleEntry1RedZone = Zone([centralSymmetry(coo, mapCenter) for coo in jungleEntry1Blue])
jungleEntry2RedZone = Zone([centralSymmetry(coo, mapCenter) for coo in jungleEntry2Blue])
jungleEntry3RedZone = Zone([centralSymmetry(coo, mapCenter) for coo in jungleEntry3Blue])
jungleEntry4RedZone = Zone([centralSymmetry(coo, mapCenter) for coo in jungleEntry4Blue])

zoneLst = [midLaneZone, jungleEntry1BlueZone, jungleEntry2BlueZone, jungleEntry3BlueZone, jungleEntry4BlueZone, topLaneZone, botLaneZone,
           jungleEntry1RedZone, jungleEntry2RedZone, jungleEntry3RedZone, jungleEntry4RedZone]

colorLst = ["b", "g", "g", "g", "g", "r", "y", "g", "g", "g", "g"]

plotZones(zoneLst, colorLst)
print(topLaneZone.containsPoint(mapCenter))

dicto = {"a":1, "b":2, "c": 3}
for key in dicto.keys():
    dicto[key] += 1
print(dicto)