from Separated.Snapshot import Snapshot
from Separated.Player import Player

class GameStat:
    def __init__(self, 
                 snapShot : Snapshot = None,
                 gameDuration : int = None,
                 begGameTime : int = None,
                 endGameTime : int = None):
        

        
        self.time = int(snapShot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)//60)
        self.playerXPDiff : list[float] = list()
        self.playerCSDiff : list[float] = list()
        self.playerGoldDiff : list[float] = list()
        self.teamGoldDiff : float = 0

        for i in range(5):
            playerOne : Player = snapShot.teamOne.players[i]
            playerTwo : Player = snapShot.teamTwo.players[i]

            self.playerXPDiff.append(playerOne.XPdiff(playerTwo))
            self.playerCSDiff.append(playerOne.CSdiff(playerTwo))
            self.playerGoldDiff.append(playerOne.goldDiff(playerTwo))

        self.teamGoldDiff = snapShot.goldDiff()
        
