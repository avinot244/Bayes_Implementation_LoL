class ObjectiveBountyPrestartEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "actualStartTime":
                self.actualStartTime = v
            elif k == "teamId":
                self.teamId = v
            elif k == "timestamp":
                self.timestamp = v