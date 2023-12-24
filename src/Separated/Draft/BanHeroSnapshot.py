from utils_stuff.converter.champion import convertToChampionName


class BanHeroSnapShot:
    def __init__(self,
                 seqIdx : int,
                 championId : int) -> None:
        self.championId = championId
        self.seqIdx = seqIdx