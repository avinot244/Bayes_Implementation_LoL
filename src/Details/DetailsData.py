import json
import pandas as pd

from utils_stuff.globals import DATA_PATH
from utils_stuff.Position import Position

from Details.PlayerSnapshot.ChampionStats import ChampionStats
from Details.PlayerSnapshot.DamageStats import DamageStats
from Details.PlayerSnapshot.PlayerSnapshotClass import PlayerSnaphotClass

from Details.GlobalEvents.BuildingKillEvent import BuildingKillEvent
from Details.GlobalEvents.ChampionKillEvent import ChampionKillEvent
from Details.GlobalEvents.EliteMonsterKillEvent import EliteMonsterKillEvent
from Details.GlobalEvents.GameEndEvent import GameEndEvent
from Details.GlobalEvents.ItemDestroyedEvent import ItemDestroyedEvent
from Details.GlobalEvents.ItemPurchasedEvent import ItemPurchasedEvent
from Details.GlobalEvents.ItemSoldEvent import ItemSoldEvent
from Details.GlobalEvents.ItemUndoEvent import ItemUndoEvent
from Details.GlobalEvents.LevelUpEvent import LevelUpEvent
from Details.GlobalEvents.ObjectiveBountyFinishEvent import ObjectiveBountyFinishEvent
from Details.GlobalEvents.ObjectiveBountyPrestartEvent import ObjectiveBountyPrestartEvent
from Details.GlobalEvents.PauseEndEvent import PauseEndEvent
from Details.GlobalEvents.SkillLevelUpEvent import SkillLevelUpEvent
from Details.GlobalEvents.TurretPlateDestroyedEvent import TurretPlateDestroyedEvent
from Details.GlobalEvents.WardKillEvent import WardKillEvent
from Details.GlobalEvents.WardPlacedEvent import WardPlacedEvent

from Details.GameEvent import GameEvent



class DetailsData:
    def __init__(self, json_path):
        # Opening and reading json file
        with open(DATA_PATH + json_path) as f:
            data = json.loads(f.read())
        df = pd.json_normalize(data)
        self.gameEventList : list[GameEvent] = list()

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

    def get_player_pathing(self, participantId : int) -> list[Position]:
        position_history : list[Position] = list()
        for frame_data in self.gameEventList:
            player_snapshot = frame_data.get_player_snapshot(participantId)
            position_history.append(player_snapshot.position)
        return position_history