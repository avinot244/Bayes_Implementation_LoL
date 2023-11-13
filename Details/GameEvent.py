from Details.PlayerSnapshot.PlayerSnapshotClass import PlayerSnaphotClass

class GameEvent:
    def __init__(self,
                 playerSnapShotList : list[PlayerSnaphotClass],
                 globalEventsList : list,
                 timeStamp : int) -> None:
        self.playerSnapShotList = playerSnapShotList
        self.globalEventsList = globalEventsList
        self.timeStamp = timeStamp

    def get_player_snapshot(self, participantId):
        for player_snapshot in self.playerSnapShotList:
            if player_snapshot.participandId == participantId:
                return player_snapshot