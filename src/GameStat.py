from Separated.Snapshot import Snapshot
from Separated.Player import Player

class GameStat:
    def __init__(self, 
                 snapShot : Snapshot = None,
                 gameDuration : int = None,
                 begGameTime : int = None,
                 endGameTime : int = None,
                 playerXPDiff : list[float] = None,
                 playerCSDiff : list[float] = None,
                 playerGoldDiff : list[float] = None,
                 teamGoldDiff : float = None):
        

        if playerXPDiff == None and playerCSDiff == None and playerGoldDiff == None and teamGoldDiff == None:
            assert snapShot != None and gameDuration != None and begGameTime != None and endGameTime != None

            self.time = int(snapShot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)//60)
            self.playerXPDiff : list[float] = list()
            self.playerCSDiff : list[float] = list()
            self.playerGoldDiff : list[float] = list()
            self.teamGoldDiff : float = 0
            # TODO : add jungle proximity

            for i in range(5):
                playerOne : Player = snapShot.teamOne.players[i]
                playerTwo : Player = snapShot.teamTwo.players[i]

                self.playerXPDiff.append(playerOne.XPdiff(playerTwo))
                self.playerCSDiff.append(playerOne.CSdiff(playerTwo))
                self.playerGoldDiff.append(playerOne.goldDiff(playerTwo))

            self.teamGoldDiff = snapShot.goldDiff()
        elif gameDuration == None and begGameTime == None and endGameTime == None and snapShot == None:
            assert playerXPDiff != None and playerCSDiff != None and playerGoldDiff != None and teamGoldDiff != None
            
            self.time = int(snapShot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)//60)
            self.playerXPDiff = playerXPDiff
            self.playerCSDiff = playerCSDiff
            self.playerGoldDiff = playerGoldDiff
            self.teamGoldDiff = teamGoldDiff
