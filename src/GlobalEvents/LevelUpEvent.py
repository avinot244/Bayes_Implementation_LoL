class LevelUpEvent:
    def __init__(self,
                 level : int,
                 participantId : int,
                 timeStamp : int) -> None:
        self.level = level
        self.participantId = participantId
        self.timeStamp = timeStamp