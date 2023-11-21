import json
import pandas as pd
import os

from utils_stuff.globals import DATA_PATH
from utils_stuff.Position import Position
from Separated.Snapshot import Snapshot
from Separated.Player import Player
from Separated.Team import Team
from Separated.Item import Item
from Separated.Stat import Stat
from tqdm import tqdm


class SeparatedData:
    def __init__(self, root_dir : str) -> None:
        self.gameSnapshotList : list[Snapshot] = list()
        self.fileNames : list[str] = list()
        self.begGameTime : int = 0
        self.endGameTime : int = 0
        print("Parsing game snapshot files from root directory {}".format(root_dir))
        for subdir, dirs, files in os.walk(root_dir):
            for file in tqdm(files):
                with open(os.path.join(subdir, file)) as f:
                    data = json.loads(f.read())
                
                df = pd.json_normalize(data)
                if df['payload.payload.type'][0] == "SNAPSHOT" and df['payload.payload.subject'][0] == "MATCH":
                    self.fileNames.append(os.path.join(subdir, file))
                    players_team_one : list[Player] = list()

                    # Parsing players for team one
                    for player_dict_team_one in df['payload.payload.payload.teamOne.players'][0]:
                        temp_items : list[Item] = list()
                        items = player_dict_team_one['items']
                        for item in items:
                            temp_item : Item = Item(item['itemID'],
                                                    item['stackSize'],
                                                    item['purchaseGameTime'],
                                                    item['cooldownRemaining'])
                            temp_items.append(temp_item)
                        player_stat_dict = player_dict_team_one['stats']
                        player_stat : Stat = Stat(player_stat_dict['minionsKilled'],
                                                player_stat_dict['championsKilled'],
                                                player_stat_dict['numDeaths'],
                                                player_stat_dict['assists'],
                                                player_stat_dict['wardPlaced'],
                                                player_stat_dict['wardKilled'],
                                                player_stat_dict['visionScore'],
                                                player_stat_dict['totalDamageDealt'],
                                                player_stat_dict['totalDamageTaken'],
                                                player_stat_dict['totalDamageSelfMitigated'],
                                                player_stat_dict['totalDamageShieldedOnTeammates'],
                                                player_stat_dict['totalDamageDealtToBuildings'],
                                                player_stat_dict['totalDamageDealtToObjectives'],
                                                player_stat_dict['totalTimeCrowdControlDealt'],
                                                player_stat_dict['totalTimeCCOthers'])
                        position_list = player_dict_team_one['position']
                        position : Position = Position(position_list[0], position_list[1])
                        temp_player : Player = Player(player_dict_team_one['championName'],
                                                    player_dict_team_one['summonerName'],
                                                    player_dict_team_one['participantID'],
                                                    player_dict_team_one['level'],
                                                    player_dict_team_one['experience'],
                                                    player_dict_team_one['attackDamage'],
                                                    player_dict_team_one['attackSpeed'],
                                                    player_dict_team_one['alive'],
                                                    player_dict_team_one['health'],
                                                    player_dict_team_one['healthRegen'],
                                                    player_dict_team_one['magicResist'],
                                                    player_dict_team_one['armor'],
                                                    player_dict_team_one['armorPenetration'],
                                                    player_dict_team_one['abilityPower'],
                                                    player_dict_team_one['currentGold'],
                                                    player_dict_team_one['totalGold'],
                                                    position,
                                                    temp_items,
                                                    player_stat)
                        players_team_one.append(temp_player)
                    
                    teamOne = Team(df['payload.payload.payload.teamOne.assists'],
                                df['payload.payload.payload.teamOne.baronKills'],
                                df['payload.payload.payload.teamOne.championsKills'],
                                df['payload.payload.payload.teamOne.deaths'],
                                df['payload.payload.payload.teamOne.dragonKills'],
                                df['payload.payload.payload.teamOne.teamID'],
                                df['payload.payload.payload.teamOne.inhibKills'],
                                df['payload.payload.payload.teamOne.totalGold'],
                                df['payload.payload.payload.teamOne.towerKills'],
                                df['payload.payload.payload.teamOne.killedDragonTypes'],
                                players_team_one)
                    
                    players_team_two : list[Player] = list()
                    # Parsing players for team two
                    for player_dict_team_two in df['payload.payload.payload.teamTwo.players'][0]:
                        temp_items : list[Item] = list()
                        items = player_dict_team_two['items']
                        for item in items:
                            temp_item : Item = Item(item['itemID'],
                                                    item['stackSize'],
                                                    item['purchaseGameTime'],
                                                    item['cooldownRemaining'])
                            temp_items.append(temp_item)
                        player_stat_dict = player_dict_team_two['stats']
                        player_stat : Stat = Stat(player_stat_dict['minionsKilled'],
                                                player_stat_dict['championsKilled'],
                                                player_stat_dict['numDeaths'],
                                                player_stat_dict['assists'],
                                                player_stat_dict['wardPlaced'],
                                                player_stat_dict['wardKilled'],
                                                player_stat_dict['visionScore'],
                                                player_stat_dict['totalDamageDealt'],
                                                player_stat_dict['totalDamageTaken'],
                                                player_stat_dict['totalDamageSelfMitigated'],
                                                player_stat_dict['totalDamageShieldedOnTeammates'],
                                                player_stat_dict['totalDamageDealtToBuildings'],
                                                player_stat_dict['totalDamageDealtToObjectives'],
                                                player_stat_dict['totalTimeCrowdControlDealt'],
                                                player_stat_dict['totalTimeCCOthers'])
                        position_list = player_dict_team_two['position']
                        position : Position = Position(position_list[0], position_list[1])
                        temp_player : Player = Player(player_dict_team_two['championName'],
                                                    player_dict_team_two['summonerName'],
                                                    player_dict_team_two['participantID'],
                                                    player_dict_team_two['level'],
                                                    player_dict_team_two['experience'],
                                                    player_dict_team_two['attackDamage'],
                                                    player_dict_team_two['attackSpeed'],
                                                    player_dict_team_two['alive'],
                                                    player_dict_team_two['health'],
                                                    player_dict_team_two['healthRegen'],
                                                    player_dict_team_two['magicResist'],
                                                    player_dict_team_two['armor'],
                                                    player_dict_team_two['armorPenetration'],
                                                    player_dict_team_two['abilityPower'],
                                                    player_dict_team_two['currentGold'],
                                                    player_dict_team_two['totalGold'],
                                                    position,
                                                    temp_items,
                                                    player_stat)
                        players_team_two.append(temp_player)

                    
                    teamTwo = Team(df['payload.payload.payload.teamTwo.assists'],
                                df['payload.payload.payload.teamTwo.baronKills'],
                                df['payload.payload.payload.teamTwo.championsKills'],
                                df['payload.payload.payload.teamTwo.deaths'],
                                df['payload.payload.payload.teamTwo.dragonKills'],
                                df['payload.payload.payload.teamTwo.teamID'],
                                df['payload.payload.payload.teamTwo.inhibKills'],
                                df['payload.payload.payload.teamTwo.totalGold'],
                                df['payload.payload.payload.teamTwo.towerKills'],
                                df['payload.payload.payload.teamTwo.killedDragonTypes'],
                                players_team_two)
                    gameSnapshot : Snapshot = Snapshot(df['payload.payload.payload.gameTime'][0], 
                                                    teamOne,
                                                    teamTwo)
                    self.gameSnapshotList.append(gameSnapshot)
                elif df['payload.payload.type'][0] == 'GAME_EVENT' and df['payload.payload.action'][0] == 'START_MAP':
                    self.begGameTime = df['payload.payload.payload.gameTime'][0]
                elif df['payload.payload.type'][0] == 'GAME_EVENT' and df['payload.payload.action'][0] == 'END_MAP':
                    self.endGameTime = df['payload.payload.payload.gameTime'][0]

    def getPlayerList(self):
        firstGameSnapshot = self.gameSnapshotList[0]
        playersTeamOne : list[str] = firstGameSnapshot.teamOne.getPlayerList()
        playersTeamTwo : list[str] = firstGameSnapshot.teamTwo.getPlayerList()
        return playersTeamOne, playersTeamTwo

    def getPlayerPositionHistory(self, participantID : int) -> list[Position]:
        positionList : list[Position] = list()  
        for gameSnapshot in self.gameSnapshotList:
            if gameSnapshot.teamOne.isPlayerInTeam(participantID):
                playerIdx : int = gameSnapshot.teamOne.getPlayerIdx(participantID)
                positionPlayer : Position = gameSnapshot.teamOne.getPlayerPosition(playerIdx)
                positionList.append(positionPlayer)
            else:
                playerIdx : int = gameSnapshot.teamTwo.getPlayerIdx(participantID)
                positionPlayer : Position = gameSnapshot.teamTwo.getPlayerPosition(playerIdx)
                positionList.append(positionPlayer)
        return positionList
    
    def getPlayerID(self, playerName : str) -> int:
        if playerName in self.gameSnapshotList[0].teamOne.getPlayerList():
            return self.gameSnapshotList[0].teamOne.getPlayerID(playerName)
        else:
            return self.gameSnapshotList[0].teamTwo.getPlayerID(playerName)