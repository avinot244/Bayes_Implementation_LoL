class ItemUndoEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "afterId":
                self.afterId = v
            elif k == "beforeId":
                self.beforeId = v
            elif k == "goldGain":
                self.goldGain = v
            elif k == "participantId":
                self.participantId = v
            elif k == "timestamp":
                self.timestamp = v