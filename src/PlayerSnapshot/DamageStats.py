class DamageStats:
    def __init__(self,
                 magicDamageDone : int = 0,
                 magicDamageDoneToChampions : int = 0,
                 magicDamageTaken : int = 0,
                 physicalDamageDone : int = 0,
                 physicalDamageDoneToChampions : int = 0,
                 physicalDamageTaken : int = 0,
                 totalDamageDone : int = 0,
                 totalDamageDoneToChampions : int = 0,
                 totalDamageTaken : int = 0,
                 trueDamageDone : int = 0,
                 trueDamageDoneToChampions : int = 0,
                 trueDamageTaken : int = 0) -> None:
        self.magicDamageDone = magicDamageDone
        self.magicDamageDoneToChampions = magicDamageDoneToChampions
        self.magicDamageTaken = magicDamageTaken
        self.physicalDamageDone = physicalDamageDone
        self.physicalDamageDoneToChampions = physicalDamageDoneToChampions
        self.physicalDamageTaken = physicalDamageTaken
        self.totalDamageDone = totalDamageDone
        self.totalDamageDoneToChampions = totalDamageDoneToChampions
        self.totalDamageTaken = totalDamageTaken
        self.trueDamageDone = trueDamageDone
        self.trueDamageDoneToChampions = trueDamageDoneToChampions
        self.trueDamageTaken = trueDamageTaken
    def getDamageStatsFromRowDict(self, rowDict):
        for k, v in rowDict.items():
            if k == "magicDamageDone":
                self.magicDamageDone = v
            elif k == "magicDamageDoneToChampions":
                self.magicDamageDoneToChampions = v
            elif k == "magicDamageTaken":
                self.magicDamageTaken = v
            elif k == "physicalDamageDone":
                self.physicalDamageDone = v
            elif k == "physicalDamageDoneToChampions":
                self.physicalDamageDoneToChampions = v
            elif k == "physicalDamageTaken":
                self.physicalDamageTaken = v
            elif k == "totalDamageDone":
                self.totalDAmageDone = v
            elif k == "totalDamageDoneToChampions":
                self.totalDamageDoneToChampions = v
            elif k == "totalDamageTaken":
                self.totalDamageTaken = v
            elif k == "trueDamaDone":
                self.trueDamaDone = v
            elif k == "trueDamageDoneToChampions":
                self.trueDamageDoneToChampions = v
            elif k == "trueDamageTaken":
                self.trueDamageTaken
    
        