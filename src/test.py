from utils_stuff.plots.plotsZone import plotZones
from AreaMapping.AreaMapping import AreaMapping


myAreaMapping = AreaMapping()

gridList = [myAreaMapping.botLanePresenceGrid,
            myAreaMapping.jungleBlueEntryPresenceGrid,]

plotZones(gridList, ["y", "g"])