class ChampionStats:
    def __init__(self,
                 rawDict : dict,) -> None:
       for k, v in rawDict.items():
            if k == "abilityHase":
                self.abilityHaste = v
            elif k == "abilityPower":
                self.abilityPower = v
            elif k == "armor":
                self.armor = v
            elif k == "armorPen":
                self.armorPen = v
            elif k == "armorPenPercent":
                self.armorPenPercent = v
            elif k == "attackDamage":
                self.attackDamage = v
            elif k == "attackSpeed": 
                self.attackSpeed = v
            elif k == "bonusArmorPenPercent":
                self.bonusArmorPenPercent = v
            elif k == "bonusMagicPenPercent":
                self.bonusMagicPenPercent = v
            elif k == "ccReduction": 
                self.ccReduction = v
            elif k == "cooldowReduction": 
                self.cooldowReduction = v
            elif k == "health":
                self.health = v
            elif k == "heatlthMax":
                self.heatlthMax = v
            elif k == "healthRegen":
                self.healthRegen = v
            elif k == "lifesteal":
                self.lifesteal = v
            elif k == "magicPen":
                self.magicPen = v
            elif k == "magicPenPercent": 
                self.magicPenPercent = v
            elif k == "magicResist":
                self.magicResist = v
            elif k == "movementSpeed":
                self.movementSpeed = v
            elif k == "omnivamp":
                self.omnivamp = v
            elif k == "physicalVamp":
                self.physicalVamp = v
            elif k == "power":
                self.power = v
            elif k == "powerMax":
                self.powerMax = v
            elif k == "powerRegen":
                self.powerRegen = v
            elif k == "spellVamp":
                self.spellVamp = v