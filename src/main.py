import pandas as pd
import json

from utils_stuff.globals import *
from utils_stuff.utils_func import *
from utils_stuff.Types import *
from Details import DetailsData
import argparse


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
    print(path)
    detailsData : DetailsData = DetailsData(path)
    print(len(detailsData.gameEventList))


# GETTING UNIQUE EVENTS
unique_events = get_all_event_types(DATA_PATH + "NORDvsBRUTE/g1/ESPORTSTMNT03_3210203_DETAILS.json")
keys = list(unique_events.keys())
keys.sort()
unique_events = {i: unique_events[i] for i in keys}

print(unique_events)

