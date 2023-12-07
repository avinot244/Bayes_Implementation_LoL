from Separated.SeparatedData import SeparatedData
from AreaMapping.Grid import Grid
from AreaMapping.Zone import Zone

from utils_stuff.globals import *
from utils_stuff.Computation.computation import centralSymmetry


class AreaMapping:
    def __init__(self) -> None:
        self.midLanePresenceGrid : Grid = Grid([Zone(midLaneBoundary)])
        self.topLanePresenceGrid : Grid = Grid([Zone(topLaneBoundary)])
        self.botLanePresenceGrid : Grid = Grid([Zone(botLaneBoundary)])
        self.jungleBlueEntryPresenceGrid : Grid = Grid([Zone(jungleEntry1Blue), Zone(jungleEntry2Blue), Zone(jungleEntry3Blue), Zone(jungleEntry4Blue)])
        self.jungleRedEntryPresenceGrid : Grid = Grid([Zone([centralSymmetry(coo, mapCenter) for coo in jungleEntry1Blue]),
                                           Zone([centralSymmetry(coo, mapCenter) for coo in jungleEntry2Blue]),
                                           Zone([centralSymmetry(coo, mapCenter) for coo in jungleEntry3Blue]),
                                           Zone([centralSymmetry(coo, mapCenter) for coo in jungleEntry4Blue])])

    def computeMapping(self, data : SeparatedData):
        ["midLanePresence", "topLanePresence", "botLanePresence", "jungleBlueEntryPresence", "jungleRedEntryPresence"]
        
        playerList = [data.gameSnapshotList[0].teamOne.getPlayerList(), data.gameSnapshotList[0].teamTwo.getPlayerList()]
        
        teamOneMapping : dict = dict()
        for playerName in playerList[0]:
            teamOneMapping[playerName] = {"midLanePresence":0, 
                                        "topLanePresence":0, 
                                        "botLanePresence":0, 
                                        "jungleBlueEntryPresence":0, 
                                        "jungleRedEntryPresence":0}
        teamTwoMapping : dict = dict()
        for playerName in playerList[1]:
            teamTwoMapping[playerName] = {"midLanePresence":0, 
                                        "topLanePresence":0, 
                                        "botLanePresence":0, 
                                        "jungleBlueEntryPresence":0, 
                                        "jungleRedEntryPresence":0}
        l = len(data.gameSnapshotList)
        for snapshot in data.gameSnapshotList:
            # For team one
            for player in snapshot.teamOne.players:
                if self.midLanePresenceGrid.containsPoint(player.position):
                    teamOneMapping[player.summonerName]['midLanePresence'] += 1
                if self.topLanePresenceGrid.containsPoint(player.position):
                    teamOneMapping[player.summonerName]['topLanePresence'] += 1
                if self.botLanePresenceGrid.containsPoint(player.position):
                    teamOneMapping[player.summonerName]['botLanePresence'] += 1
                if self.jungleBlueEntryPresenceGrid.containsPoint(player.position):
                    teamOneMapping[player.summonerName]['jungleBlueEntryPresence'] += 1
                if self.jungleRedEntryPresenceGrid.containsPoint(player.position):
                    teamOneMapping[player.summonerName]['jungleRedEntryPresence'] += 1
            
            # For team two
            for player in snapshot.teamTwo.players:
                if self.midLanePresenceGrid.containsPoint(player.position):
                    teamTwoMapping[player.summonerName]['midLanePresence'] += 1
                if self.topLanePresenceGrid.containsPoint(player.position):
                    teamTwoMapping[player.summonerName]['topLanePresence'] += 1
                if self.botLanePresenceGrid.containsPoint(player.position):
                    teamTwoMapping[player.summonerName]['botLanePresence'] += 1
                if self.jungleBlueEntryPresenceGrid.containsPoint(player.position):
                    teamTwoMapping[player.summonerName]['jungleBlueEntryPresence'] += 1
                if self.jungleRedEntryPresenceGrid.containsPoint(player.position):
                    teamTwoMapping[player.summonerName]['jungleRedEntryPresence'] += 1

        
        for playerName, mapping in teamOneMapping.items():
            for key in mapping.keys():
                mapping[key] /= l
            