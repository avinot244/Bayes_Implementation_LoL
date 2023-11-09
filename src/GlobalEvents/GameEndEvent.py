class GameEndEvent:
    def __init__(self,
                 gameId : int,
                 realTimeStamp : int,
                 timeStamp : int,
                 winningTeam : int) -> None:
        self.gameId = gameId
        self.realTimeStamp = realTimeStamp
        self.timeStamp = timeStamp
        self.winningTeam = winningTeam
        