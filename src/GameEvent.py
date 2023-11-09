from PlayerSnapshot.PlayerSnapshot import PlayerSnapshot

class GameEvent:
    def __init__(self,
                 playerSnapShotList : list,
                 globalEventsList : list,
                 timeStamp : int) -> None:
        self.playerSnapShotList = playerSnapShotList
        self.globalEventsList = globalEventsList
        self.timeStamp = timeStamp