class GameEndEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "gameId":
                self.gameId = v
            elif k == "realTimeStamp":
                self.realTimeStamp = v
            elif k == " timestamp":
                self.timestamp = v
            elif k == "winningTeam":
                self.winningTeam = v
