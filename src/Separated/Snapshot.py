from Separated.Team import Team 

class Snapshot:
    def __init__(self,
                 filename : str,
                 gameTime : int,
                 teamOne : Team,
                 teamTwo : Team):
        self.filename = filename
        self.gameTime = gameTime
        self.teamOne = teamOne
        self.teamTwo = teamTwo
    
    def convertGameTimeToSeconds(self, gameDuration : int, begGameTime : int, endGameTime : int):
        return ((self.gameTime - begGameTime)*gameDuration)/(endGameTime - begGameTime)
    
    def goldDiff(self):
        return self.teamOne.totalGold - self.teamTwo.totalGold