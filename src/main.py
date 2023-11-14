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
    

    path = DATA_PATH + match + "/" + game + "/" + "ESPORTSTMNT03_3228010_DETAILS.json"
    detailsData : DetailsData = DetailsData(path)
    path = DATA_PATH + match + "/" + game + "/" + "ESPORTSTMNT03_3228010_SUMMARY.json"
    summaryData : SummaryData = SummaryData(path)

    plot_player_position(1, detailsData, "positionsZeus")
    plot_player_position(2, detailsData, "positionsOner")
    plot_player_position(3, detailsData, "positionsFaker")
    plot_player_position(4, detailsData, "positionsGumayusi")
    plot_player_position(5, detailsData, "positionsKeria")

    plot_player_position(6, detailsData, "positions369")
    plot_player_position(7, detailsData, "positionsKanavi")
    plot_player_position(8, detailsData, "positionsKnight")
    plot_player_position(9, detailsData, "positionsRuler")
    plot_player_position(10, detailsData, "positionsMissing")
    
    

