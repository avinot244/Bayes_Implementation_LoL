from Separated.Snapshot import Snapshot
from Separated.Player import Player

class GameStat:
    def __init__(self, 
                 snapShot : Snapshot,
                 gameDuration : int,
                 begGameTime : int,
                 endGameTime : int):
        
        self.time = int(snapShot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)//60)
        self.playerXPDiff : list[int] = list()
        self.playerCSDiff : list[int] = list()
        self.playerGoldDiff : list[int] = list()
        self.teamGoldDiff : list[int] = list()
        # TODO : add jungle proximity

        for i in range(5):
            playerOne : Player = snapShot.teamOne.players[i]
            playerTwo : Player = snapShot.teamTwo.players[i]

            self.playerXPDiff.append(playerOne.XPdiff(playerTwo))
            self.playerCSDiff.append(playerOne.CSdiff(playerTwo))
            self.playerGoldDiff.append(playerOne.goldDiff(playerTwo))

        self.teamGoldDiff.append(snapShot.goldDiff())
