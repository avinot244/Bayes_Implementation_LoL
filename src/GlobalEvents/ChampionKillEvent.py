from utils_stuff.Position import Position
from utils_stuff.DamageRecap import DamageRecap

class ChampionKillEvent:
    def __init__(self, rawDict : dict) -> None:
        for k, v in rawDict.items():
            if k == "assistingParticipantIds":
                self.assistingParticipantIds : list = v
            elif k == "bounty":
                self.bounty : int = v
            elif k == "killStreakLength":
                self.killStreakLength : int = v
            elif k == "position":
                self.position : Position = Position()
                self.position.getPositionFromRawDict(v)
            elif k == "shutdownBounty":
                self.shutdownBounty = v
            elif k == "timestamp":
                self.timestamp = v
            elif k == "victimDamageDealt":
                self.victimDamageDealt : list = list()
                for damage_recap_dict in v:
                    self.victimDamageDealt.append(DamageRecap(damage_recap_dict))
            elif k == "victimDamageReceived":
                self.victimDamageReceived : list = list()
                for damage_recap_dict in self.victimDamageReceived:
                    self.victimDamageReceived.append(DamageRecap(damage_recap_dict))
            elif k == "victimId":
                self.victimId : int = v