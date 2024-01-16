from Separated.Game.SeparatedData import SeparatedData
from AreaMapping.Grid import Grid
from AreaMapping.Zone import Zone

from utils_stuff.globals import *
from utils_stuff.Computation.computation import centralSymmetry


class AreaMapping:
    def __init__(self) -> None:
        self.midLanePresenceGrid : Grid = Grid([Zone(midLaneBoundary)])
        self.topLanePresenceGrid : Grid = Grid([Zone(topLaneBoundary)])
        self.botLanePresenceGrid : Grid = Grid([Zone(botLaneBoundary)])
        self.jungleBlueEntryPresenceGrid : Grid = Grid([Zone(jungleEntry1Blue), 
                                                        Zone(jungleEntry2Blue), 
                                                        Zone(jungleEntry3Blue), 
                                                        Zone(jungleEntry4Blue)])
        self.jungleRedEntryPresenceGrid : Grid = Grid([Zone(jungleEntry1Red),
                                                       Zone(jungleEntry2Red),
                                                       Zone(jungleEntry3Red),
                                                       Zone(jungleEntry4Red)])
        
        self.riverBotPresenceGrid : Grid = Grid([Zone(riverBot)])
        self.riverTopPresenceGrid : Grid = Grid([Zone(riverTop)])
        self.jungleBlueTopPresenceGrid : Grid = Grid([Zone(jungleBlueTop)])
        self.jungleBlueBotPresenceGrid : Grid = Grid([Zone(jungleBlueBot)])
        self.jungleRedTopPresenceGrid : Grid = Grid([Zone(jungleRedTop)])
        self.jungleRedBotPresenceGrid : Grid = Grid([Zone(jungleRedBot)])
        
        self.forwardMidBlue : list[Grid] = None
        self.forwardMidRed : list[Grid] = None
        # For forward % we can do a list of grid for each lane where in each grid we have the forward degree zone
        
        self.teamOneMapping : dict = dict()
        self.teamTwoMapping : dict = dict()
    
    def computeMapping(self, data : SeparatedData):
        
        playerList = [data.gameSnapshotList[0].teamOne.getPlayerList(), data.gameSnapshotList[0].teamTwo.getPlayerList()]
        
        for summonerName in playerList[0]:
            self.teamOneMapping[summonerName] = {"midLanePresence":0, 
                                                "topLanePresence":0, 
                                                "botLanePresence":0, 
                                                "jungleAllyEntryPresence":0, 
                                                "jungleEnemyEntryPresence":0,
                                                "riverBotPresence":0,
                                                "riverTopPresence":0,
                                                "jungleAllyTopPresence":0,
                                                "jungleAllyBotPresence":0,
                                                "jungleEnemyTopPresence":0,
                                                "jungleEnemyBotPresence":0}
        for summonerName in playerList[1]:
            self.teamTwoMapping[summonerName] = {"midLanePresence":0, 
                                                "topLanePresence":0, 
                                                "botLanePresence":0, 
                                                "jungleEnemyEntryPresence":0, 
                                                "jungleAllyEntryPresence":0,
                                                "riverBotPresence":0,
                                                "riverTopPresence":0,
                                                "jungleAllyTopPresence":0,
                                                "jungleAllyBotPresence":0,
                                                "jungleEnemyTopPresence":0,
                                                "jungleEnemyBotPresence":0}
        l = len(data.gameSnapshotList)
        for snapshot in data.gameSnapshotList:
            # For team one
            for player in snapshot.teamOne.players:
                if self.midLanePresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['midLanePresence'] += 1
                if self.topLanePresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['topLanePresence'] += 1
                if self.botLanePresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['botLanePresence'] += 1
                if self.jungleBlueEntryPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['jungleAllyEntryPresence'] += 1
                if self.jungleRedEntryPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['jungleEnemyEntryPresence'] += 1
                
                if self.riverBotPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['riverBotPresence'] += 1
                if self.riverTopPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['riverTopPresence'] += 1

                if self.jungleBlueTopPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['jungleAllyTopPresence'] += 1
                if self.jungleBlueBotPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['jungleAllyBotPresence'] += 1
                if self.jungleRedTopPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['jungleEnemyTopPresence'] += 1
                if self.jungleRedBotPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.summonerName]['jungleEnemyBotPresence'] += 1
            
            # For team two
            for player in snapshot.teamTwo.players:
                if self.midLanePresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['midLanePresence'] += 1
                if self.topLanePresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['topLanePresence'] += 1
                if self.botLanePresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['botLanePresence'] += 1
                if self.jungleBlueEntryPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['jungleEnemyEntryPresence'] += 1
                if self.jungleRedEntryPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['jungleAllyEntryPresence'] += 1

                if self.riverBotPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['riverBotPresence'] += 1
                if self.riverTopPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['riverTopPresence'] += 1

                if self.jungleBlueTopPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['jungleEnemyTopPresence'] += 1
                if self.jungleBlueBotPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['jungleEnemyBotPresence'] += 1
                if self.jungleRedTopPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['jungleAllyTopPresence'] += 1
                if self.jungleRedBotPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.summonerName]['jungleAllyBotPresence'] += 1
        
        for summonerName, mapping in self.teamOneMapping.items():
            for key in mapping.keys():
                mapping[key] /= l
        for summonerName, mapping in self.teamTwoMapping.items():
            for key in mapping.keys():
                mapping[key] /= l
            