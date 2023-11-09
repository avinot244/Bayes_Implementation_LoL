class ChampionStats:
    def __init__(self,
                 abilityHaste : int = 0,
                 abilityPower : int = 0,
                 armor : int = 0,
                 armorPen : int = 0,
                 armorPenPercet : int = 0,
                 attackDamage : int = 0,
                 attackSpeed : int = 0,
                 bonusArmorPenPercent : int = 0,
                 bonusMagicPenPercent : int = 0,
                 ccReduction : int = 0,
                 cooldownReduction : int = 0,
                 health : int = 0,
                 healthMax : int = 0,
                 healthRegen : int = 0,
                 lifesteal : int = 0,
                 magicPen : int = 0,
                 magicPenPercent : int = 0,
                 magicResist : int = 0,
                 movementSpeed : int = 0,
                 omnivamp : int = 0,
                 physicalVamp : int = 0,
                 power : int = 0,
                 powerMax : int = 0,
                 powerRegen : int = 0,
                 spellVamp : int = 0) -> None:
        self.abilityHaste = abilityHaste
        self.abilityPower = abilityPower
        self.armor = armor
        self.armorPen = armorPen
        self.armorPenPercet = armorPenPercet
        self.attackDamage = attackDamage
        self.attackSpeed = attackSpeed
        self.bonusArmorPenPercent = bonusArmorPenPercent
        self.bonusMagicPenPercent = bonusMagicPenPercent
        self.ccReduction = ccReduction
        self.cooldownReduction = cooldownReduction
        self.health = health
        self.healthMax = healthMax
        self.healthRegen = healthRegen
        self.lifesteal = lifesteal
        self.magicPen = magicPen
        self.magicPenPercent = magicPenPercent
        self.magicResist = magicResist
        self.movementSpeed = movementSpeed
        self.omnivamp = omnivamp
        self.physicalVamp = physicalVamp
        self.power = power
        self.powerMax = powerMax
        self.powerRegen = powerRegen
        self.spellVamp = spellVamp

    def getChampionStatsFromRowDict(self, rowDict : dict):
        for k, v in rowDict.items():
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