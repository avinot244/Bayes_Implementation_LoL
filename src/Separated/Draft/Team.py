from Separated.Draft.Player import Player

class Team:
    def __init__(self,
                 players : list[Player]) -> None:
        self.players = players