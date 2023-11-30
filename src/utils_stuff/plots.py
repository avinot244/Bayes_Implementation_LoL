import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

from Separated.SeparatedData import SeparatedData
from utils_stuff.globals import *

def createGrayScale(length : int):
    grayScale : list[float] = list()
    for i in range(length):
        value = i/length
        grayScale.append([value, value, value])
    return grayScale

def plot_player_position(positionList : list[Position], figName : str, path : str):
    X = [pos.x for pos in positionList]
    Y = [pos.y for pos in positionList]

    towerRedX = [pos.x for pos in towerPositionRedSide]
    towerRedY = [pos.y for pos in towerPositionRedSide]
    towerBlueX = [pos.x for pos in towerPositionBlueSide]
    towerBlueY = [pos.y for pos in towerPositionBlueSide]

    inhibitorRedX = [pos.x for pos in inhibitorPositionRedSide]
    inhibitorRedY = [pos.y for pos in inhibitorPositionRedSide]
    inhibitorBlueX = [pos.x for pos in inhibitorPositionBlueSide]
    inhibitorBlueY = [pos.y for pos in inhibitorPositionBlueSide]

    img = np.asarray(Image.open("../Summoner's_Rift_Minimap.webp"))

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, MINIMAP_WIDTH, 0, MINIMAP_HEIGHT])

    grayScale = createGrayScale(len(X))
    X.reverse()
    Y.reverse()
    grayScale.reverse()
    ax.scatter(X, Y, s = [10], c=grayScale)
    plt.scatter(towerRedX, towerRedY, color="Red", s=[100])
    plt.scatter(towerBlueX, towerBlueY, color="Blue", s=[100])
    
    plt.scatter(inhibitorRedX, inhibitorRedY, color="Orange", s=[100])
    plt.scatter(inhibitorBlueX, inhibitorBlueY, color="Cyan", s=[100])

    ax.set_aspect("equal", adjustable="box")
    plt.axis('off')
    plt.savefig(path + "{}.png".format(figName))
    plt.close()


def plot_multiple_players_positions_animated(positionLists : list[list[Position]], colorList : list[str], markerList : list[str], figName : str, path : str):
    subteamLength = len(positionLists)//2
    assert figName != "" and path != ""

    towerRedX = [pos.x for pos in towerPositionRedSide]
    towerRedY = [pos.y for pos in towerPositionRedSide]
    towerBlueX = [pos.x for pos in towerPositionBlueSide]
    towerBlueY = [pos.y for pos in towerPositionBlueSide]

    inhibitorRedX = [pos.x for pos in inhibitorPositionRedSide]
    inhibitorRedY = [pos.y for pos in inhibitorPositionRedSide]
    inhibitorBlueX = [pos.x for pos in inhibitorPositionBlueSide]
    inhibitorBlueY = [pos.y for pos in inhibitorPositionBlueSide]

    img = np.asarray(Image.open("../Summoner's_Rift_Minimap.webp"))

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, MINIMAP_WIDTH, 0, MINIMAP_HEIGHT])
    plt.scatter(towerRedX, towerRedY, color="Red", s=[100])
    plt.scatter(towerBlueX, towerBlueY, color="Blue", s=[100])
    
    plt.scatter(inhibitorRedX, inhibitorRedY, color="Orange", s=[100])
    plt.scatter(inhibitorBlueX, inhibitorBlueY, color="Cyan", s=[100])
    ax.set_aspect("equal", adjustable="box")
    plt.axis('off')

    scatters = []

    for i in range(len(positionLists)):
        if i < subteamLength:
            scatters.append(ax.scatter([], [], color=colorList[i%subteamLength], s=[25], marker=markerList[i%subteamLength]))
        else:
            scatters.append(ax.scatter([], [], color=colorList[i%subteamLength], s=[25], marker=markerList[5+i%subteamLength]))
    def update(frame):
        for i in range(len(positionLists)):
            X = [pos.x for pos in positionLists[i]]
            Y = [pos.y for pos in positionLists[i]]
            if frame > 10:   
                x = X[frame-10:frame]
                y = Y[frame-10:frame]
            else:
                x = X[:frame]
                y = Y[:frame]
            
            data = np.stack([x, y]).T
            scatters[i].set_offsets(data)
        return scatters
    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(positionLists[0]), interval=200)
    writervideo = animation.FFMpegWriter(fps=60) 
    ani.save(path + figName + '.mp4', writer=writervideo) 
    plt.close()

def plot_player_position_animated(positionList : list[Position], figName : str):
    X = [pos.x for pos in positionList]
    Y = [pos.y for pos in positionList]

    towerRedX = [pos.x for pos in towerPositionRedSide]
    towerRedY = [pos.y for pos in towerPositionRedSide]
    towerBlueX = [pos.x for pos in towerPositionBlueSide]
    towerBlueY = [pos.y for pos in towerPositionBlueSide]

    inhibitorRedX = [pos.x for pos in inhibitorPositionRedSide]
    inhibitorRedY = [pos.y for pos in inhibitorPositionRedSide]
    inhibitorBlueX = [pos.x for pos in inhibitorPositionBlueSide]
    inhibitorBlueY = [pos.y for pos in inhibitorPositionBlueSide]

    img = np.asarray(Image.open("../Summoner's_Rift_Minimap.webp"))

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, MINIMAP_WIDTH, 0, MINIMAP_HEIGHT])

    scat = ax.scatter(X[0], Y[0], color="white", s=[5])

    def update(frame):
        if frame > 10:
            x = X[frame-10:frame]
            y = Y[frame-10:frame]
        else:
            x = X[:frame]
            y = Y[:frame]
        data = np.stack([x, y]).T
        scat.set_offsets(data)
        return scat
    plt.scatter(towerRedX, towerRedY, color="Red", s=[100])
    plt.scatter(towerBlueX, towerBlueY, color="Blue", s=[100])
    
    plt.scatter(inhibitorRedX, inhibitorRedY, color="Orange", s=[100])
    plt.scatter(inhibitorBlueX, inhibitorBlueY, color="Cyan", s=[100])
    ax.set_aspect("equal", adjustable="box")
    plt.axis('off')

    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(X), interval=200)
    writervideo = animation.FFMpegWriter(fps=60) 
    ani.save(figName + '.mp4', writer=writervideo) 
    plt.close()

        

def plotTeamPosition(playerNameList : list[str], data : SeparatedData, name : str, path : str):
    
    for playerName in playerNameList:
        participantID = data.getPlayerID(playerName)
        positionHistory = data.getPlayerPositionHistory(participantID)
        playerName = playerName.replace(' ', '_')
        plot_player_position(positionHistory, name + "_{}".format(playerName))


def plotTeamPositionAnimated(playerNameList : list[str], data : SeparatedData):
    for playerName in playerNameList:
        participantID = data.getPlayerID(playerName)
        positionHistory = data.getPlayerPositionHistory(participantID)
        playerName = playerName.replace(' ', '_')
        plot_player_position_animated(positionHistory, "positions_{}".format(playerName))
    
def plotAllTeamPositionAnimated(playerNameList : list[str], data : SeparatedData, name : str, path : str):
    positionLists : list[list[Position]] = list()
    for playerName in playerNameList:
        participantID = data.getPlayerID(playerName)
        positionHistory = data.getPlayerPositionHistory(participantID)
        playerName = playerName.replace(' ', '_')
        positionLists.append(positionHistory)
    colorList = ["blue", "green", "red", "yellow", "purple"]
    markerList = ["o"]*5
    plot_multiple_players_positions_animated(positionLists, colorList, markerList, name, path)

def plotBothTeamsPositionAnimated(playerNameListTeamOne : list[str], playerNameListTeamTwo : list[str], data : SeparatedData, name : str, path : str):
    positionLists : list[list[Position]] = list()
    # Getting positions for team one
    for playerName in playerNameListTeamOne:
        participantID = data.getPlayerID(playerName)
        positionHistory = data.getPlayerPositionHistory(participantID)
        playerName = playerName.replace(' ', '_')
        positionLists.append(positionHistory)
    
    # Getting positions for team two
    for playerName in playerNameListTeamTwo:
        participantID = data.getPlayerID(playerName)
        
        positionHistory = data.getPlayerPositionHistory(participantID)
        playerName = playerName.replace(' ', '_')
        positionLists.append(positionHistory)
    colorList = ["blue", "green", "red", "yellow", "purple"] * 2
    markerList = ["o"] * 5 + ["^"] * 5
    plot_multiple_players_positions_animated(positionLists, colorList, markerList, name, path)
