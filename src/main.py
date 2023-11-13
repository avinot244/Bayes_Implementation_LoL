# clear && python3 main.py --match NORDvsBRUTE --game 1 --file DETAILS


import pandas as pd
import json
from PIL import Image
import argparse
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes


from utils_stuff.globals import *
from utils_stuff.utils_func import *
from utils_stuff.Types import *

from Details.DetailsData import DetailsData
from Summary.SummaryData import SummaryData





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--match", metavar="[NORDvsBRUTE]", required=True, help="Match to analyse")
    parser.add_argument("-g", "--game", metavar="[1|2|3|4|5]", required=True, help="Game to analyse")
    parser.add_argument("-f", "--file", metavar="[DETAILS | SUMMARY]", required=True, help="If you want to have summary or detail json loaded")
    args = parser.parse_args()
    args_data = vars(args)

    match = ""
    game = ""
    file = ""

    for arg, value in args_data.items():
        if arg == "match":
            match = value
        if arg == "game":
            game = "g{}".format(value)
        if arg == "file":
            file = value
    path = DATA_PATH + match + "/" + game + "/" + "ESPORTSTMNT03_3210203_{}.json".format(file)
    detailsData : DetailsData = DetailsData(path)

    pathing = detailsData.get_player_pathing(1)
    X = [pos.x for pos in pathing]
    Y = [pos.y for pos in pathing]


    towerRedX = [pos.x for pos in towerPositionRedSide]
    towerRedY = [pos.y for pos in towerPositionRedSide]
    towerBlueX = [pos.x for pos in towerPositionBlueSide]
    towerBlueY = [pos.y for pos in towerPositionBlueSide]

    inhibitorRedX = [pos.x for pos in inhibitorPositionRedSide]
    inhibitorRedY = [pos.y for pos in inhibitorPositionRedSide]
    inhibitorBlueX = [pos.x for pos in inhibitorPositionBlueSide]
    inhibitorBlueY = [pos.y for pos in inhibitorPositionBlueSide]

    img = np.asarray(Image.open("../Summoner's_Rift_Minimap.webp"))

    fig, ax =plt.subplots()
    ax.imshow(img, extent=[0, MINIMAP_WIDTH, 0, MINIMAP_HEIGHT])


    ax.scatter(X, Y, color="white")
    plt.scatter(towerRedX, towerRedY, color="Red", s=[100])
    plt.scatter(towerBlueX, towerBlueY, color="Blue", s=[100])
    
    plt.scatter(inhibitorRedX, inhibitorRedY, color="Orange", s=[100])
    plt.scatter(inhibitorBlueX, inhibitorBlueY, color="Cyan", s=[100])

    ax.set_aspect("equal", adjustable="box")
    plt.savefig("temp.png")

    path = DATA_PATH + match + "/" + game + "/" + "ESPORTSTMNT03_3210203_SUMMARY.json"
    summaryData : SummaryData = SummaryData(path)
    

