import pandas as pd
import json

from utils_stuff.globals import *
from utils_stuff.utils_func import *
from utils_stuff.Types import *
from Details import DetailsData

path_summary = "g1/ESPORTSTMNT03_3210203_SUMMARY.json"
path_details = "g1/ESPORTSTMNT03_3210203_DETAILS.json"



# PARSING ALL GAME SNAPSHOTS
with open(DATA_PATH + "g1/ESPORTSTMNT03_3210203_DETAILS.json", 'r') as f:
    data = json.loads(f.read())
df = pd.json_normalize(data)



detailsData : DetailsData = DetailsData(path_details)
print(len(detailsData.gameEventList))



# GETTING UNIQUE EVENTS

unique_events = get_all_event_types(DATA_PATH + "g1/ESPORTSTMNT03_3210203_DETAILS.json")
keys = list(unique_events.keys())
keys.sort()
unique_events = {i: unique_events[i] for i in keys}







    


# for game_snapshot in df['frames'][0]:
#     print("\n-------------------\n")
#     print(game_snapshot)
#     event_list = game_snapshot['events']
#     participant_frame_updates = game_snapshot['participantFrames']


