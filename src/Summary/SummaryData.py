import json
import pandas as pd

from utils_stuff.globals import DATA_PATH

from Summary.PlayerEndGameStat import PlayerEndGameStat
from Summary.TeamEndGameStat import TeamEndGameStat

class SummaryData:
    def __init__(self, json_path):
        with open(DATA_PATH + json_path) as f:
            data = json.loads(f.read())
        df = pd.json_normalize(data)
        self.gameCreation : int = df['gameCreation'][0]
        self.gameDuration : int = df['gameDuration'][0]
        self.gameEndTimestamp : int = df['gameEndTimestamp'][0]
        self.gameId : int = df['gameId'][0]
        self.gameMode : str = df['gameMode'][0]
        self.gameName : str = df['gameName'][0]
        self.gameStartTimestamp : int = df['gameStartTimestamp'][0]
        self.gameType : str = df['gameType'][0]
        self.gameVersion : str = df['gameVersion'][0]
        self.mapId : int = df['mapId'][0]

        self.participants : list[PlayerEndGameStat] = list()

        self.platformId : str = df['platformId'][0]
        self.queueId : int = df['queueId'][0]
        self.seasonId : int = df['seasonId'][0]
        
        self.teams : list[TeamEndGameStat] = list()

        self.tournamentCode : str = df['tournamentCode'][0]

        for participant in df['participants'][0]:
            print("\n----------------\n")
            print(participant)
