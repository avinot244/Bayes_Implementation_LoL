import json
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
from datetime import datetime

from EMH.Details.DetailsData import DetailsData
from Separated.SeparatedData import SeparatedData
from utils_stuff.globals import *


def get_all_event_types(json_path_details:str) -> dict:
    with open(json_path_details, 'r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data)
    frames = df['frames'][0]
    
    unique_event_type : dict = dict()
    for frame in frames: # Looping throug every frame snapshot
        events = frame['events']
        for event in events: # Looping throug every event of that snapshot
            event_attributes = list(event.keys())
            if not(event['type'] in list(unique_event_type.keys())):
                unique_event_type[event['type']] = event_attributes
        
    
    for (_, v) in unique_event_type.items():
        v.remove('type')
    
    return unique_event_type
        
def abs_dist(position1 : Position, position2 : Position) -> float:
    return math.sqrt(np.abs(position2.x - position1.x)**2 + np.abs(position2.y - position1.y)**2)

def createGrayScale(length : int):
    grayScale : list[float] = list()
    for i in range(length):
        value = i/length
        grayScale.append([value, value, value])
    return grayScale

def plot_player_position(positionList : list[Position], figName : str):
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
    plt.savefig("{}.png".format(figName))
    plt.close()


def plot_multiple_players_positions_animated(positionLists : list[list[Position]], colorList : list[str], figName : str):
    assert len(positionLists) == len(colorList)
    assert figName != ""

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

    scatters = [ax.scatter([], [], color=colorList[i], s=[5]) for i in range(len(positionLists))]

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
    ani.save(figName + '.mp4', writer=writervideo) 
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

        

def plotTeamPosition(playerNameList : list[str], data : SeparatedData):
    for playerName in playerNameList:
        participantID = data.getPlayerID(playerName)
        positionHistory = data.getPlayerPositionHistory(participantID)
        playerName = playerName.replace(' ', '_')
        plot_player_position(positionHistory, "positions_{}".format(playerName))

def plotTeamPositionAnimated(playerNameList : list[str], data : SeparatedData):
    for playerName in playerNameList:
        participantID = data.getPlayerID(playerName)
        positionHistory = data.getPlayerPositionHistory(participantID)
        playerName = playerName.replace(' ', '_')
        plot_player_position_animated(positionHistory, "positions_{}".format(playerName))
    
def plotAllTeamPositionAnimated(playerNameList : list[str], data : SeparatedData):
    positionLists : list[list[Position]] = list()
    for playerName in playerNameList:
        participantID = data.getPlayerID(playerName)
        positionHistory = data.getPlayerPositionHistory(participantID)
        playerName = playerName.replace(' ', '_')
        positionLists.append(positionHistory)
    colorList = ["blue", "green", "yellow", "red", "white"]
    plot_multiple_players_positions_animated(positionLists, colorList, "positions_T1")


def convert_into_real_time(timestampBeg : int, timestampEnd : int):
    dateBeg = datetime.fromtimestamp(timestampBeg/1000.0)
    print(dateBeg)

    dateEnd = datetime.fromtimestamp(timestampEnd/1000.0)
    print(dateEnd)

    return dateBeg, dateEnd



