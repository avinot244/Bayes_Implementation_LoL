from Separated.Draft.BanHeroSnapshot import BanHeroSnapShot
from Separated.Draft.SelectedHeroSnapshot import SelectedHeroSnapshot
from Separated.Draft.DraftSnapshot import DraftSnapshot

class Draft:
    def __init__(self,
                 picks : list[SelectedHeroSnapshot],
                 bans : list[BanHeroSnapShot],
                 data : list[DraftSnapshot]) -> None:
        self.picks = picks
        self.bans = bans
        self.data = data

