import pandas as pd
import json

from utils_stuff.globals import *
from utils_stuff.Position import Position
from utils_stuff.utils_func import *
from utils_stuff.Types import *
from PlayerSnapshot.PlayerSnapshotClass import PlayerSnaphotClass
from PlayerSnapshot.ChampionStats import ChampionStats
from PlayerSnapshot.DamageStats import DamageStats
from GlobalEvents.BuildingKillEvent import BuildingKillEvent
# from GlobalEvents.ChampionKillEvent import ChampionKillEvent TODO : implement ChampionKillEvent
from GlobalEvents.EliteMonsterKillEvent import EliteMonsterKillEvent
from GlobalEvents.GameEndEvent import GameEndEvent
from GlobalEvents.ItemDestroyedEvent import ItemDestroyedEvent
from GlobalEvents.ItemPurchasedEvent import ItemPurchasedEvent
from GlobalEvents.ItemSoldEvent import ItemSoldEvent
from GlobalEvents.ItemUndoEvent import ItemUndoEvent
from GlobalEvents.LevelUpEvent import LevelUpEvent
from GlobalEvents.ObjectiveBountyFinishEvent import ObjectiveBountyFinishEvent
from GlobalEvents.ObjectiveBountyPrestartEvent import ObjectiveBountyPrestartEvent
from GlobalEvents.PauseEndEvent import PauseEndEvent
from GlobalEvents.SkillLevelUpEvent import SkillLevelUpEvent
from GlobalEvents.TurretPlateDestroyedEvent import TurretPlateDestroyedEvent
from GlobalEvents.WardKillEvent import WardKillEvent
from GlobalEvents.WardPlacedEvent import WardPlacedEvent
from GameEvent import GameEvent

path_summary = DATA_PATH + "/ESPORTSTMNT03_3210203_SUMMARY.json"

def parse_event_type(eventDict):
    event_type = eventDict['type']
    res = None
    if event_type == "BUILDING_KILL":
        res = BuildingKillEvent(eventDict)
    elif event_type == "CHAMPION_KILL":
        print("TODO champion kill event")
    elif event_type == "ELITE_MONSTER_KILL":
        res = EliteMonsterKillEvent(eventDict)
    elif event_type == "GAME_END":
        res = GameEndEvent(eventDict)
    elif event_type == "ITEM_DESTROYED":
        res = ItemDestroyedEvent(eventDict)
    elif event_type == "ITEM_PURCHASED":
        res = ItemPurchasedEvent(eventDict)
    elif event_type == "ITEM_SOLD":
        res = ItemSoldEvent(eventDict)
    elif event_type == "ITEM_UNDO":
        res = ItemUndoEvent(eventDict)
    elif event_type == "LEVEL_UP":
        res = LevelUpEvent(eventDict)
    elif event_type == "OBJECTIVE_BOUNTY_FINISH":
        res = ObjectiveBountyFinishEvent(eventDict)
    elif event_type == "OBJECTIVE_BOUNTY_PRESTART":
        res = ObjectiveBountyPrestartEvent(eventDict)
    elif event_type == "PAUSE_END":
        res = PauseEndEvent(eventDict)
    elif event_type == "SKILL_LEVEL_UP":
        res = SkillLevelUpEvent(eventDict)
    elif event_type == "TURRET_PLATE_DESTROYED":
        res = TurretPlateDestroyedEvent(eventDict)
    elif event_type == "WARD_KILL":
        res = WardKillEvent(eventDict)
    elif event_type == "WARD_PLACED":
        res = WardPlacedEvent(eventDict)

    return res





# GETTING UNIQUE EVENTS

unique_events = get_all_event_types(DATA_PATH + "/ESPORTSTMNT03_3210203_DETAILS.json")
keys = list(unique_events.keys())
keys.sort()
unique_events = {i: unique_events[i] for i in keys}


# PARSING FIRST GAME SNAPSHOT
with open(DATA_PATH + "/ESPORTSTMNT03_3210203_DETAILS.json", 'r') as f:
    data = json.loads(f.read())
df = pd.json_normalize(data)

gameEventList : list = list()

print(len(df["frames"][0]))

for frame in df['frames'][0]:
    participant_frame_updates = frame['participantFrames']
    event_frame_updates = frame['events']
    frame_timestamp = frame['timestamp']
    playerSnapShotList : list = list()
    globalEventList : list = list()

    for participant_id, participant_data in participant_frame_updates.items():
        championStats = ChampionStats(participant_data["championStats"])
        damageStats = DamageStats(participant_data["damageStats"])
        position = Position()
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


    for event in event_frame_updates:
        globalEventList.append(parse_event_type(event))

    gameEvent = GameEvent(playerSnapShotList, globalEventList, frame_timestamp)
    gameEventList.append(gameEvent)

print(len(gameEventList))

    


# for game_snapshot in df['frames'][0]:
#     print("\n-------------------\n")
#     print(game_snapshot)
#     event_list = game_snapshot['events']
#     participant_frame_updates = game_snapshot['participantFrames']


