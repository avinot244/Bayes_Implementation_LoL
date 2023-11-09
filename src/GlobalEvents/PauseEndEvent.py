class PauseEndEvent:
    def __init__(self,
                 realTimeStamp : int,
                 timeStamp : int) -> None:
        self.realTimeStamp = realTimeStamp
        self.timeStamp = timeStamp