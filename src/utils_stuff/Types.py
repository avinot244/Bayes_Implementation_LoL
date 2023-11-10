from enum import Enum
class TowerType(Enum):
    OuterTurret = "OUTER_TURRET"
    InnerTurret = "INNER_TURRET"
    BaseTurret = "BASE_TURRET"
    NexusTurret = "NEXUS_TURRET"


class LaneType(Enum):
    TopLane = "TOP_LANE"
    MidLane = "MID_LANE"
    BotLane = "BOT_LANE"

class MonsterSubType(Enum):
    HextechDragon = "HEXTECH_DRAGON" # TODO : complete with all other types

class MonsterType(Enum):
    Dragon = "DRAGON" # TODO : complete with all other types

class LevelUpType(Enum):
    Normal = "NORMAL" # TODO : complete with all other types

class WardType(Enum):
    ControlWard = "CONTROL_WARD" # TODO : complete with all other types
    YellowTrinket = "YELLOW_TRINKET"

class BuildingType(Enum):
    TowerBuilding = "TOWER_BUILDING" # TODO : complete with all other types