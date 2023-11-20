from Separated.Team import Team 

class Snapshot:
    def __init__(self,
                 gameTime : int,
                 teamOne : Team,
                 teamTwo : Team):
        self.gameTime = gameTime
        self.teamOne = teamOne
        self.teamTwo = teamTwo