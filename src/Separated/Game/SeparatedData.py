import ujson
import pandas as pd
import os
import csv

from utils_stuff.globals import DATA_PATH
from utils_stuff.Position import Position
from Separated.Game.Snapshot import Snapshot
from Separated.Game.Player import Player as separatedPlayer
from Separated.Game.Team import Team as separatedTeam
from Separated.Game.Item import Item
from Separated.Game.Stat import Stat

from Separated.Draft.DraftSnapshot import DraftSnapshot
from Separated.Draft.BanHeroSnapshot import BanHeroSnapShot
from Separated.Draft.SelectedHeroSnapshot import SelectedHeroSnapshot
from Separated.Draft.Draft import Draft
from Separated.Draft.Player import Player as draftPlayer
from Separated.Draft.Team import Team as draftTeam

from utils_stuff.converter.champion import convertToChampionName

from tqdm import tqdm


class SeparatedData:
    def __init__(self, root_dir : str = None, 
                 gameSnapShotList : list[Snapshot] = None,
                 begGameTime : int = 0,
                 endGameTime : int = 0) -> None:
        self.matchName = root_dir.split('/')[2]
        
        if not(gameSnapShotList is None) and not(begGameTime == 0) and not(endGameTime == 0):
            self.gameSnapshotList = gameSnapShotList
            self.begGameTime = begGameTime
            self.endGameTime = endGameTime
        elif not(root_dir is None):
            self.gameSnapshotList : list[Snapshot] = list()
            self.begGameTime : int = 0
            self.endGameTime : int = 0

            tempBans : list[BanHeroSnapShot] = list()
            tempPicks : list[SelectedHeroSnapshot] = list()
            tempDraftSnapshotList : list[DraftSnapshot] = list()

            print("Parsing game snapshot files from root directory {}".format(root_dir))
            for subdir, dirs, files in os.walk(root_dir, topdown=True):
                l = lambda s : s[:-5]
                files = [l(f) for f in files]
                for file in tqdm(sorted(files, key=int)):
                    with open(os.path.join(subdir, file + ".json")) as f:
                        data = ujson.loads(f.read())
                    
                    df = pd.json_normalize(data)
                    if df['payload.payload.type'][0] == "SNAPSHOT" and df['payload.payload.subject'][0] == "MATCH":
                        # Getting the winning team
                        if df['payload.payload.payload.gameOver'][0]:
                            if df['payload.payload.payload.winningTeam'][0] == 100:
                                self.winningTeam = 0
                            else:
                                self.winningTeam = 1 
                        
                        players_team_one : list[separatedPlayer] = list()

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
                            temp_player : separatedPlayer = separatedPlayer(player_dict_team_one['championName'],
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
                        
                        teamOne = separatedTeam(df['payload.payload.payload.teamOne.assists'],
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
                        
                        players_team_two : list[separatedPlayer] = list()
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
                            temp_player : separatedPlayer = separatedPlayer(player_dict_team_two['championName'],
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

                        
                        teamTwo = separatedTeam(df['payload.payload.payload.teamTwo.assists'],
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
                        gameSnapshot : Snapshot = Snapshot(file,
                                                           df['seqIdx'],
                                                        df['payload.payload.payload.gameTime'][0], 
                                                        teamOne,
                                                        teamTwo)
                        self.gameSnapshotList.append(gameSnapshot)
                        self.matchId : str = df['payload.payload.payload.name'][0]
                    elif df['payload.payload.type'][0] == 'GAME_EVENT' and df['payload.payload.action'][0] == 'START_MAP':
                        self.begGameTime = df['payload.payload.payload.gameTime'][0]
                    elif df['payload.payload.type'][0] == 'GAME_EVENT' and df['payload.payload.action'][0] == 'END_MAP':
                        self.endGameTime = df['payload.payload.payload.gameTime'][0]
                    elif df['payload.payload.type'][0] == 'GAME_EVENT' and df['payload.payload.action'][0] == 'BANNED_HERO':
                        
                        
                        banHeroSnapShot : BanHeroSnapShot = BanHeroSnapShot(df['seqIdx'][0],
                                                                            df['payload.payload.payload.championId'].to_list()[0])
                        tempBans.append(banHeroSnapShot)
                    elif df['payload.payload.type'][0] == 'GAME_EVENT' and df['payload.payload.action'][0] == 'SELECTED_HERO':
                        selectedHeroSnapshot : SelectedHeroSnapshot = SelectedHeroSnapshot(df['seqIdx'][0],
                                                                                           df['payload.payload.payload.championId'].to_list()[0])
                        tempPicks.append(selectedHeroSnapshot)
                    elif df['payload.payload.type'][0] == 'SNAPSHOT' and df['payload.payload.subject'][0] == 'TEAM':
                        teamOneData : list[draftPlayer] = list()
                        for player_dict_team_one in df['payload.payload.payload.teamOne.players'][0]:
                            teamOneData.append(draftPlayer(player_dict_team_one['championID'], player_dict_team_one['summonerName']))
                        teamOne : draftTeam = draftTeam(teamOneData)

                        teamTwoData : list[draftPlayer] = list()
                        for player_dict_team_two in df['payload.payload.payload.teamTwo.players'][0]:
                            teamTwoData.append(draftPlayer(player_dict_team_two['championID'], player_dict_team_two['summonerName']))
                        teamTwo : draftTeam = draftTeam(teamTwoData)

                        draftSnapshot : DraftSnapshot = DraftSnapshot(df['seqIdx'].to_list()[0], file, teamOne, teamTwo)
                        tempDraftSnapshotList.append(draftSnapshot)
                    
            self.draft : Draft = Draft(tempPicks, tempBans, tempDraftSnapshotList)
        else:
            print("Invalid arguments passed")


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
                if gameSnapshot.teamOne.players[playerIdx].isAlive():
                    positionPlayer : Position = gameSnapshot.teamOne.getPlayerPosition(playerIdx)
                    positionList.append(positionPlayer)
            else:
                playerIdx : int = gameSnapshot.teamTwo.getPlayerIdx(participantID)
                if gameSnapshot.teamTwo.players[playerIdx].isAlive():
                    positionPlayer : Position = gameSnapshot.teamTwo.getPlayerPosition(playerIdx)
                    positionList.append(positionPlayer)
        return positionList
    
    

    def getPlayerID(self, playerName : str) -> int:
        assert playerName in self.gameSnapshotList[0].teamOne.getPlayerList() or playerName in self.gameSnapshotList[0].teamTwo.getPlayerList()
        if playerName in self.gameSnapshotList[0].teamOne.getPlayerList():
            return self.gameSnapshotList[0].teamOne.getPlayerID(playerName)
        else:
            return self.gameSnapshotList[0].teamTwo.getPlayerID(playerName)
        
    
    def splitData(self, gameDuration : int, splitList : list[int]):
        snapshotListTemp : list[list[Snapshot]] = [[] for _ in range(len(splitList))]
        res : list[SeparatedData] = list() # List of len 1+len(splitList)
        for snapshot in self.gameSnapshotList:
            snapshotTime = snapshot.convertGameTimeToSeconds(gameDuration, self.begGameTime, self.endGameTime)
            for i in range(len(splitList)):
                if snapshotTime < splitList[i]:
                    snapshotListTemp[i].append(snapshot)
                    break
        for snapshotLst in snapshotListTemp:
            res.append(SeparatedData(gameSnapShotList=snapshotLst, begGameTime=self.begGameTime, endGameTime=self.endGameTime))
        return res
    
    def getSnapShotByTime(self, time : float, gameDuration : int):
        """Gets snapshot where time is the closest"""
        begGameTime = self.begGameTime
        endGameTime = self.endGameTime

        firstSnapShotTime = self.gameSnapshotList[0].convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)
        delta = abs(time - firstSnapShotTime)
        idx = 0
        for i in range(len(self.gameSnapshotList)):
            snapShotTime = self.gameSnapshotList[i].convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)
            tempDelta = abs(time - snapShotTime)
            if tempDelta < delta:
                delta = tempDelta
                idx = i
        
        return self.gameSnapshotList[idx]
    
    def getTeamNames(self) -> dict:
        teamName : dict = dict()
        firstSnapShot = self.gameSnapshotList[0]
        teamNameOne = firstSnapShot.teamOne.players[0].summonerName.split(' ')[0]
        teamNameTwo = firstSnapShot.teamTwo.players[0].summonerName.split(' ')[0]
        teamName[teamNameOne] = 0
        teamName[teamNameTwo] = 1
        return teamName

    def draftToCSV(self, path : str, new : bool, patch: str):
        # Asserting the right open option
        if new:
            open_option = 'w+'
        else:
            open_option = 'a+'
        
        # Writing the draft pick order database   
        full_path = path + "draft_pick_order.csv"
        with open(full_path, open_option) as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            if new :
                header = ["Patch", "MatchName", "MatchId", "Winner", "BB1", "BB2", "BB3", "BB4", "BB5", "BP1", "BP2", "BP3", "BP4", "BP5", "RB1", "RB2", "RB3", "RB4", "RB5", "RP1", "RP2", "RP3", "RP4", "RP5"]
                writer.writerow(header)
            
            data : list = list()
            data.append(patch)
            data.append(self.matchName)
            data.append(self.matchId)
            data.append(self.winningTeam)

            if len(self.draft.bans) < 10 :
                for i in range(10-len(self.draft.bans)):
                    self.draft.bans.append(BanHeroSnapShot(-1, -1))
            
            if len(self.draft.picks) < 10:
                for i in range(10-len(self.draft.picks)):
                    self.draft.picks.append(BanHeroSnapShot(-1, -1))

            # Getting data for bans for blue side
            data.append(convertToChampionName(self.draft.bans[0].championId))
            data.append(convertToChampionName(self.draft.bans[2].championId))
            data.append(convertToChampionName(self.draft.bans[4].championId))
            data.append(convertToChampionName(self.draft.bans[6].championId))
            data.append(convertToChampionName(self.draft.bans[8].championId))
            # Getting data for picks for blue side
            data.append(convertToChampionName(self.draft.picks[0].championId))
            data.append(convertToChampionName(self.draft.picks[3].championId))
            data.append(convertToChampionName(self.draft.picks[4].championId))
            data.append(convertToChampionName(self.draft.picks[7].championId))
            data.append(convertToChampionName(self.draft.picks[9].championId))
            # Getting data for bans for red side
            data.append(convertToChampionName(self.draft.bans[1].championId))
            data.append(convertToChampionName(self.draft.bans[3].championId))
            data.append(convertToChampionName(self.draft.bans[5].championId))
            data.append(convertToChampionName(self.draft.bans[7].championId))
            data.append(convertToChampionName(self.draft.bans[9].championId))
            # Getting data for pick for red side
            data.append(convertToChampionName(self.draft.picks[1].championId))
            data.append(convertToChampionName(self.draft.picks[2].championId))
            data.append(convertToChampionName(self.draft.picks[5].championId))
            data.append(convertToChampionName(self.draft.picks[6].championId))
            data.append(convertToChampionName(self.draft.picks[8].championId))
            
            writer.writerow(data)
        
        full_path = path + "draft_player_picks.csv"

        # Writing the draft player picks database
        with open(full_path, open_option) as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            data : list = list()
            if new :
                header = ['Patch', 'MatchName', 'MatchId', 'SummonerName', 'championName']
                writer.writerow(header)
            

            
            maxSeqIdx : int = self.draft.data[0].seqIdx
            idx : int = 0
            for i in range(len(self.draft.data)):
                if self.draft.data[i].seqIdx > maxSeqIdx:
                    maxSeqIdx = self.draft.data[i].seqIdx
                    idx = i
                
            lastDraftSnapshot = self.draft.data[idx]
            # Getting data for team one 
            for player in lastDraftSnapshot.teamOne.players:
                data.append(patch)
                data.append(self.matchName)
                data.append(self.matchId)
                data.append(player.summonerName)
                data.append(convertToChampionName(player.championID))
            
                writer.writerow(data)
                data = []

            for player in lastDraftSnapshot.teamTwo.players:
                data.append(patch)
                data.append(self.matchName)
                data.append(self.matchId)
                data.append(player.summonerName)
                data.append(convertToChampionName(player.championID))

                writer.writerow(data)
                data = []