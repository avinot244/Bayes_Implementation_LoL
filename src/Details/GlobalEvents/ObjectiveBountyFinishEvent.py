class ObjectiveBountyFinishEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "teamId":
                self.teamId = v
            elif k == "timestamp":
                self.timestamp = v