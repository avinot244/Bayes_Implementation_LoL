import pandas as pd
from utils_stuff.globals import *
import json
from utils_stuff.Position import Position
from utils_stuff.utils_func import *
from utils_stuff.Types import *
from PlayerSnapshot.PlayerSnapshotClass import PlayerSnaphotClass
from PlayerSnapshot.ChampionStats import ChampionStats
from PlayerSnapshot.DamageStats import DamageStats

path_summary = DATA_PATH + "/ESPORTSTMNT03_3210203_SUMMARY.json"



unique_events = get_all_event_types(DATA_PATH + "/ESPORTSTMNT03_3210203_DETAILS.json")
keys = list(unique_events.keys())
keys.sort()
unique_events = {i: unique_events[i] for i in keys}
# for (event_name, event_attributes) in unique_events.items():
#     print("{} : {}".format(event_name, event_attributes))

with open(DATA_PATH + "/ESPORTSTMNT03_3210203_DETAILS.json", 'r') as f:
    data = json.loads(f.read())
df = pd.json_normalize(data)

first_game_snapshot = df['frames'][0][1]
event_list = first_game_snapshot['events']
participant_frame_updates = first_game_snapshot['participantFrames']

print("event list :", event_list)
print("\n------------------\n")
print("participants list :", participant_frame_updates)
print(type(participant_frame_updates))

playerSnapShotList = list()
test = ChampionStats()

for participant_id, participant_data in participant_frame_updates.items():
    championStats = ChampionStats()
    damageStats = DamageStats()
    position = Position()
    championStats.getChampionStatsFromRowDict(participant_data["championStats"])
    damageStats.getDamageStatsFromRowDict(participant_data["damageStats"])
    position.getPositionFromRawDict(participant_data["position"])
    playerSnapShot = PlayerSnaphotClass(int(participant_id),
                                        championStats,
                                        participant_data["currentGold"],
                                        damageStats,
                                        participant_data["goldPerSecond"],
                                        participant_data["jungleMinionsKilled"],
                                        participant_data["level"],
                                        participant_data["minionsKilled"],
                                        participant_data["participantId"],
                                        position,
                                        participant_data["timeEnemySpentControlled"],
                                        participant_data["totalGold"],
                                        participant_data["xp"])
    playerSnapShotList.append(playerSnapShot)


# for game_snapshot in df['frames'][0]:
#     print("\n-------------------\n")
#     print(game_snapshot)
#     event_list = game_snapshot['events']
#     participant_frame_updates = game_snapshot['participantFrames']


