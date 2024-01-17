import json
import pandas as pd

from utils_stuff.globals import DATA_PATH

from EMH.Summary.PlayerEndGameStat import PlayerEndGameStat
from EMH.Summary.TeamEndGameStat import TeamEndGameStat
from EMH.Summary.Ban import Ban
from EMH.Summary.Objective import Objective

class SummaryData:
    def __init__(self, json_path : str):
        with open(json_path) as f:
            data = json.loads(f.read())
        df = pd.json_normalize(data)
        self.patch : str = df['gameVersion'][0]
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
            participantEndGameStat = PlayerEndGameStat(participant['assistMePings'],
                                                       participant['assists'],
                                                       participant['baronKills'],
                                                       participant['basicPings'],
                                                       participant['bountyLevel'],
                                                       participant['champExperience'],
                                                       participant['champLevel'],
                                                       participant['championId'],
                                                       participant['championName'],
                                                       participant['championTransform'],
                                                       participant['commandPings'],
                                                       participant['consumablesPurchased'],
                                                       participant['damageDealtToBuildings'],
                                                       participant['damageDealtToObjectives'],
                                                       participant['damageDealtToTurrets'],
                                                       participant['damageSelfMitigated'],
                                                       participant['dangerPings'],
                                                       participant['deaths'],
                                                       participant['detectorWardsPlaced'],
                                                       participant['doubleKills'],
                                                       participant['dragonKills'],
                                                       participant['eligibleForProgression'],
                                                       participant['enemyMissingPings'],
                                                       participant['enemyVisionPings'],
                                                       participant['firstBloodAssist'],
                                                       participant['firstBloodKill'],
                                                       participant['firstTowerAssist'],
                                                       participant['firstTowerKill'],
                                                       participant['gameEndedInEarlySurrender'],
                                                       participant['gameEndedInSurrender'],
                                                       participant['getBackPings'],
                                                       participant['goldEarned'],
                                                       participant['goldSpent'],
                                                       participant['holdPings'],
                                                       participant['individualPosition'],
                                                       participant['inhibitorKills'],
                                                       participant['inhibitorTakedowns'],
                                                       participant['inhibitorsLost'],
                                                       participant['item0'],
                                                       participant['item1'],
                                                       participant['item2'],
                                                       participant['item3'],
                                                       participant['item4'],
                                                       participant['item5'],
                                                       participant['item6'],
                                                       participant['itemsPurchased'],
                                                       participant['killingSprees'],
                                                       participant['kills'],
                                                       participant['lane'],
                                                       participant['largestCriticalStrike'],
                                                       participant['largestKillingSpree'],
                                                       participant['largestMultiKill'],
                                                       participant['longestTimeSpentLiving'],
                                                       participant['magicDamageDealt'],
                                                       participant['magicDamageDealtToChampions'],
                                                       participant['magicDamageTaken'],
                                                       participant['needVisionPings'],
                                                       participant['neutralMinionsKilled'],
                                                       participant['nexusKills'],
                                                       participant['nexusLost'],
                                                       participant['nexusTakedowns'],
                                                       participant['objectivesStolen'],
                                                       participant['objectivesStolenAssists'],
                                                       participant['onMyWayPings'],
                                                       participant['participantId'],
                                                       participant['pentaKills'],
                                                       participant['physicalDamageDealt'],
                                                       participant['physicalDamageDealtToChampions'],
                                                       participant['physicalDamageTaken'],
                                                       participant['profileIcon'],
                                                       participant['pushPings'],
                                                       participant['quadraKills'],
                                                       participant['role'],
                                                       participant['sightWardsBoughtInGame'],
                                                       participant['spell1Casts'],
                                                       participant['spell1Id'],
                                                       participant['spell2Casts'],
                                                       participant['spell2Id'],
                                                       participant['spell3Casts'],
                                                       participant['spell4Casts'],
                                                       participant['subteamPlacement'],
                                                       participant['summoner1Casts'],
                                                       participant['summoner2Casts'],
                                                       participant['summonerId'],
                                                       participant['summonerLevel'],
                                                       participant['summonerName'],
                                                       participant['teamEarlySurrendered'],
                                                       participant['teamId'],
                                                       participant['teamPosition'],
                                                       participant['timeCCingOthers'],
                                                       participant['timePlayed'],
                                                       participant['totalAllyJungleMinionsKilled'],
                                                       participant['totalDamageDealt'],
                                                       participant['totalDamageDealtToChampions'],
                                                       participant['totalDamageShieldedOnTeammates'],
                                                       participant['totalDamageTaken'],
                                                       participant['totalEnemyJungleMinionsKilled'],
                                                       participant['totalHeal'],
                                                       participant['totalHealsOnTeammates'],
                                                       participant['totalMinionsKilled'],
                                                       participant['totalTimeCCDealt'],
                                                       participant['totalTimeSpentDead'],
                                                       participant['totalUnitsHealed'],
                                                       participant['tripleKills'],
                                                       participant['trueDamageDealt'],
                                                       participant['trueDamageDealtToChampions'],
                                                       participant['trueDamageTaken'],
                                                       participant['turretKills'],
                                                       participant['turretTakedowns'],
                                                       participant['turretsLost'],
                                                       participant['unrealKills'],
                                                       participant['visionClearedPings'],
                                                       participant['visionScore'],
                                                       participant['visionWardsBoughtInGame'],
                                                       participant['wardsKilled'],
                                                       participant['wardsPlaced'],
                                                       participant['win'])
            self.participants.append(participantEndGameStat)
        
        for team in df['teams'][0]:
            bans = team['bans']
            objectives  : dict = team['objectives']
            
            banList : list[Ban] = list()
            for ban in bans :
                banObject = Ban(ban['championId'],
                                ban['pickTurn'])
                banList.append(banObject)
            
            objectiveList : list[Objective] = list()
            for objectiveName, objectiveStat in objectives.items():
                objectiveObject = Objective(objectiveName,
                                            objectiveStat['first'],
                                            objectiveStat['kills'])
                objectiveList.append(objectiveObject)
            
            teamObject = TeamEndGameStat(banList, objectiveList,
                                         team['teamId'],
                                         team['win'])
            self.teams.append(teamObject)