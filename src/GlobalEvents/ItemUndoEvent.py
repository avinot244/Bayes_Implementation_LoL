class ItemUndoEvent:
    def __init__(self,
                 afterId : int,
                 beforeId : int,
                 goldGain : int,
                 participantId : int,
                 timeStamp : int) -> None:
        self.afterId = afterId
        self.beforeId = beforeId
        self.goldGain = goldGain
        self.participantId = participantId
        self.timeStamp = timeStamp