from EMH.Summary.Ban import Ban
from EMH.Summary.Objective import Objective

class TeamEndGameStat:
    def __init__(self,
                 bans : list[Ban],
                 objectives : list[Objective],
                 teamId : int,
                 win : bool) -> None:
        self.bans = bans
        self.objectives = objectives
        self.teamId = teamId
        self.win = win