from utils_stuff.converter.champion import convertToChampionName

class SelectedHeroSnapshot:
    def __init__(self,
                 seqIdx : int,
                 championId : int) -> None:
        self.championId = championId
        self.seqIdx = seqIdx