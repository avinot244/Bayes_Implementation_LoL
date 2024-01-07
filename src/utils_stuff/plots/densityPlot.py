import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from PIL import Image

from Separated.Game.SeparatedData import SeparatedData
from utils_stuff.Position import Position
from utils_stuff.globals import *


def getPositionsMultipleGames(participantNames : list[str], dataLst : list[SeparatedData]):
    # Getting player positions
    participantPositions : list[Position] = list()

    for data in dataLst:
        participantIds : list[int] = [data.getPlayerID(playerName) for playerName in participantNames]
        for playerId in participantIds:
            participantPositions += data.getPlayerPositionHistory(playerId)
    
    return participantPositions

def getPositionsSingleGame(participantNames : list[str], data : SeparatedData):
    # Getting player positions
    participantIds : list[int] = [data.getPlayerID(playerName) for playerName in participantNames]
    participantPositions : list[Position] = list()
    
    for playerId in participantIds:
        participantPositions += data.getPlayerPositionHistory(playerId)

    return participantPositions

def densityPlot(participantPositions : list[Position], graphName : str, save_path : str):
    # Splitting positions and adding map borders to it
    x = [(lambda pos : pos.x)(pos) for pos in participantPositions]
    x.append(0)
    x.append(MINIMAP_WIDTH)
    x = np.array(x)

    y = [(lambda pos : pos.y)(pos) for pos in participantPositions]
    y.append(0)
    y.append(MINIMAP_HEIGHT)
    y = np.array(y)

    # Evaluate a gaussian Kernel density estimation on our positions
    nbins = 300
    k = gaussian_kde([x, y])
    xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j] # Meshing our positions
    zi = k(np.vstack([xi.flatten(), yi.flatten()])) # Making a kernel density estimation with a gaussian projection

    
    # Making the plot
    fig, ax = plt.subplots()
    plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto', zorder=-1)

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
    plt.colorbar(ax=ax, location='right', label="density")
    plt.title(graphName)
    plt.savefig("{}/{}.png".format(save_path, graphName))
    plt.clf()