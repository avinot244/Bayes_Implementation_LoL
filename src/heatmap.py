import numpy as np
import matplotlib.pyplot as plt

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
    print(len(all_position), len(positionHistoryTemp))



x = [(lambda pos : pos.x)(pos) for pos in all_position]
y = [(lambda pos : pos.y)(pos) for pos in all_position]

fig, ax = plt.subplots()

# Plotting the position heatmap
h = ax.hist2d(x, y, bins=[np.arange(0,MINIMAP_WIDTH,150), np.arange(0,MINIMAP_HEIGHT,150)], alpha = 1, zorder=-1)
# plt.show()
fig.colorbar(h[3], ax=ax)

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