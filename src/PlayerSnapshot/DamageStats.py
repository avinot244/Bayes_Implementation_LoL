class DamageStats:
    def __init__(self,
                 rawDict : int) -> None:
        for k, v in rawDict.items():
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
                self.trueDamageTaken = v
    
        