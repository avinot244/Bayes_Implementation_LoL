class ItemSoldEvent:
    def __init__(self,
                 itemId : int,
                 participantId : int,
                 timeStamp : int) -> None:
        self.itemId = itemId
        self.participantId = participantId
        self.timeStamp = timeStamp