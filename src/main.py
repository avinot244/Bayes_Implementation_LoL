# clear && python3 main.py --match NORDvsBRUTE --game 1 --file DETAILS
# clear && python3 main.py --match JDGvsT1 --game 1 --file DETAILS

import argparse
import os
import json
import pandas as pd
import pickle

from utils_stuff.globals import *
from utils_stuff.utils_func import *
from utils_stuff.Types import *

from EMH.Details.DetailsData import DetailsData
from EMH.Summary.SummaryData import SummaryData
from Separated.SeparatedData import SeparatedData




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
    

    # path = DATA_PATH + match + "/" + game + "/" + "ESPORTSTMNT03_3228010_DETAILS.json"
    # detailsData : DetailsData = DetailsData(path)
    # path = DATA_PATH + match + "/" + game + "/" + "ESPORTSTMNT03_3228010_SUMMARY.json"
    # summaryData : SummaryData = SummaryData(path)

    rootdir = '../data/JDGvsT1/{}/Separated'.format(game)
    

    # with open(rootdir + "/8905.json", 'r') as f:
    #     data = json.loads(f.read())
    # df = pd.json_normalize(data)


    data = SeparatedData(rootdir)
 
    pathData = DATA_PATH + match + game + "data"
    file = open(pathData, 'ab')
    pickle.dump(data, file)
    file.close()
    

    # for player in df['payload.payload.payload.teamOne.players'][0]:
    #     print("\n------------\n")
    #     print(player)

    # for subdir, dirs, files in os.walk(rootdir):
    #     for file in files:
    #         with open(os.path.join(subdir, file)) as f:
    #             data = json.loads(f.read())
    #         df = pd.json_normalize(data)
            