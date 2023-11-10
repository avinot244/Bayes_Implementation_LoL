class DamageRecap:
    def __init__(self, rawDic : dict) -> None:
        for k, v in rawDic.items():
            if k == "basic":
                self.basic : bool = v
            elif k == "magicDamage":
                self.magicDamage : int = v
            elif k == "name":
                self.name : str = v
            elif k == "participantId":
                self.participantId : int = v
            elif k == "physicalDamage":
                self.physicalDamage : int = v
            elif k == "spellName":
                self.spellName : str = v
            elif k == "spellSlot":
                self.spellSlot : int = v
            elif k == "trueDamage":
                self.trueDamage : int = v