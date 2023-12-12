import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

from EMH.Summary.SummaryData import SummaryData
from utils_stuff.utils_func import *
from utils_stuff.globals import *
from utils_stuff.globals import *
from PIL import Image
from Separated.Snapshot import Snapshot
from GameStat import GameStat

yamlParser : YamlParer = YamlParer("./config.yml")

match = yamlParser.ymlDict['match']
rootdir = yamlParser.ymlDict['brute_data'] + "{}/".format(match)

dirList : list[str] = list()

for subdir, dirs, _ in os.walk(rootdir):
    dirList.append(dirs)

nbGameBo = len(dirList[0])
gameList = dirList[0]
all_position : list[Position] = []

for gameIdx in gameList:
    subRootdir = yamlParser.ymlDict['brute_data'] + "/{}/{}".format(yamlParser.ymlDict['match'], gameIdx)
    pathData = yamlParser.ymlDict['brute_data'] + yamlParser.ymlDict['match'] + gameIdx + "data"

    summaryDataTemp : SummaryData = getSummaryData(subRootdir)
            
    gameNumber = gameIdx.split("g")[1]
    (separatedDataTemp, gameDuration, begGameTime, endGameTime) = getData(False, yamlParser, gameNumber)
    splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
    splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
    if splitList[-1] > gameDuration:
        splitList[-1] = gameDuration
    else:
        splitList.append(gameDuration)
    
    
    splittedDatasetTemp : list[SeparatedData] = separatedDataTemp.splitData(summaryDataTemp.gameDuration, splitList)
    
    participantID : int = splittedDatasetTemp[1].getPlayerID("T1 Oner")
    positionHistoryTemp = splittedDatasetTemp[1].getPlayerPositionHistory(participantID)
    all_position += positionHistoryTemp

# Splitting positions and adding map borders to it
x = [(lambda pos : pos.x)(pos) for pos in all_position]
x.append(0)
x.append(MINIMAP_WIDTH)
y = [(lambda pos : pos.y)(pos) for pos in all_position]
y.append(0)
y.append(MINIMAP_HEIGHT)

x = np.array(x)
y = np.array(y)

fig, ax = plt.subplots()


# Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
nbins=300
k = gaussian_kde([x,y])
xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j] # Meshing our positions
zi = k(np.vstack([xi.flatten(), yi.flatten()])) # Making a kernel density estimation with a gaussian projection

# Make the plot
plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto', zorder=-1)
# plt.colorbar()

# Plotting minimap
img = np.asarray(Image.open("../Summoner's_Rift_MinimapTransparent.webp"))
ax.imshow(img, extent=[0, MINIMAP_WIDTH, 0, MINIMAP_HEIGHT])

towerRedX = [pos.x for pos in towerPositionRedSide]
towerRedY = [pos.y for pos in towerPositionRedSide]
towerBlueX = [pos.x for pos in towerPositionBlueSide]
towerBlueY = [pos.y for pos in towerPositionBlueSide]

inhibitorRedX = [pos.x for pos in inhibitorPositionRedSide]
inhibitorRedY = [pos.y for pos in inhibitorPositionRedSide]
inhibitorBlueX = [pos.x for pos in inhibitorPositionBlueSide]
inhibitorBlueY = [pos.y for pos in inhibitorPositionBlueSide]

plt.scatter(towerRedX, towerRedY, color="Red", s=[100])
plt.scatter(towerBlueX, towerBlueY, color="Blue", s=[100])

plt.scatter(inhibitorRedX, inhibitorRedY, color="Orange", s=[100])
plt.scatter(inhibitorBlueX, inhibitorBlueY, color="Cyan", s=[100])
ax.set_aspect("equal", adjustable="box")
plt.axis('off')



plt.savefig("position_heatmap.png")