from Separated.Team import Team 

class Snapshot:
    def __init__(self,
                 gameTime : int,
                 teamOne : Team,
                 teamTwo : Team):
        self.gameTime = gameTime
        self.teamOne = teamOne
        self.teamTwo = teamTwo
    def convertGameTimeToSeconds(self, gameDuration : int, begGameTime : int, endGameTime : int):
        return ((self.gameTime - begGameTime)*gameDuration)/(endGameTime - begGameTime)