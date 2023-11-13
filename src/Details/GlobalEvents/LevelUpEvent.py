class LevelUpEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "level":
                self.level = v
            elif k == "participantId":
                self.participantId = v
            elif k == "timestamp":
                self.timestamp = v