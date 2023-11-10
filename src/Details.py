import json
import pandas as pd

from utils_stuff.globals import DATA_PATH
from utils_stuff.Position import Position

from PlayerSnapshot.ChampionStats import ChampionStats
from PlayerSnapshot.DamageStats import DamageStats
from PlayerSnapshot.PlayerSnapshotClass import PlayerSnaphotClass

from GlobalEvents.BuildingKillEvent import BuildingKillEvent
from GlobalEvents.ChampionKillEvent import ChampionKillEvent
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



class DetailsData:
    def __init__(self, json_path):
        # Opening and reading json file
        with open(DATA_PATH + json_path) as f:
            data = json.loads(f.read())
        df = pd.json_normalize(data)
        print(df)
        self.gameEventList : list = list()

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
                globalEventList.append(self.parse_event_type(event))

            gameEvent = GameEvent(playerSnapShotList, globalEventList, frame_timestamp)
            self.gameEventList.append(gameEvent)
    
    def parse_event_type(self, eventDict):
        event_type = eventDict['type']
        res = None
        if event_type == "BUILDING_KILL":
            res = BuildingKillEvent(eventDict)
        elif event_type == "CHAMPION_KILL":
            res = ChampionKillEvent(eventDict)
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
