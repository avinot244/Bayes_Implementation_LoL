class PauseEndEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "realTimestamp":
                self.realTimestamp = v
            elif k == "timestamp":
                self.timestamp = v