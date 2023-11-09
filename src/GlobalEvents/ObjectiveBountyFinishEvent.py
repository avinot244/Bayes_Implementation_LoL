class ObjectiveBountyFinishEvent:
    def __init__(self,
                 teamId : int,
                 timeStamp : int) -> None:
        self.teamId = teamId 
        self.timeStamp = timeStamp