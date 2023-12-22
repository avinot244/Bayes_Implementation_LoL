import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

from Separated.Game.SeparatedData import SeparatedData
from utils_stuff.globals import *
from AreaMapping.Grid import Grid

def plotZones(grid : Grid, colorLst : list[str]):
    img = np.asarray(Image.open("../Summoner's_Rift_Minimap.webp"))

    _, ax = plt.subplots()

    towerRedX = [pos.x for pos in towerPositionRedSide]
    towerRedY = [pos.y for pos in towerPositionRedSide]
    towerBlueX = [pos.x for pos in towerPositionBlueSide]
    towerBlueY = [pos.y for pos in towerPositionBlueSide]

    inhibitorRedX = [pos.x for pos in inhibitorPositionRedSide]
    inhibitorRedY = [pos.y for pos in inhibitorPositionRedSide]
    inhibitorBlueX = [pos.x for pos in inhibitorPositionBlueSide]
    inhibitorBlueY = [pos.y for pos in inhibitorPositionBlueSide]

    ax.imshow(img, extent=[0, MINIMAP_WIDTH, 0, MINIMAP_HEIGHT])
    plt.scatter(towerRedX, towerRedY, color="Red", s=[100])
    plt.scatter(towerBlueX, towerBlueY, color="Blue", s=[100])
    
    plt.scatter(inhibitorRedX, inhibitorRedY, color="Orange", s=[100])
    plt.scatter(inhibitorBlueX, inhibitorBlueY, color="Cyan", s=[100])

    for i in range(len(grid.zoneList)):
        zone = grid.zoneList[i]
        X : list = [(lambda pos : pos.x)(pos) for pos in zone.boundary]
        Y : list = [(lambda pos : pos.y)(pos) for pos in zone.boundary]
        X.append(X[0])
        Y.append(Y[0])
        plt.plot(X,Y,"{}-".format(colorLst[i]))
    # plt.show()
    plt.savefig("temp.png")
