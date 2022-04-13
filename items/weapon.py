from items.item import Item
from random import uniform
class Weapon(Item):
    def __init__(self, name: str, value: int, weight: float,base_dmg: int, dmg_type: str, crit_mod: float,variance: float,traits: list) -> None:
        super().__init__(name, value, weight)
        self.base_dmg = base_dmg
        self.dmg_type = dmg_type
        self.crit_mod = crit_mod
        self.traits = traits
        self.variance = variance
    
    async def getType(self):
        return "Weapon"
    
    async def getBaseDamage(self):
        return self.base_dmg
    
    async def getCriticalModifier(self):
        return self.crit_mod
    
    async def dealDamage(self,STR=0,criticalHit=False):
        critBonus = (self.crit_mod - 1.00) if criticalHit == True else 0.00
        return int((self.base_dmg + STR) * uniform(1 - self.variance + critBonus, 1 + self.variance + critBonus))

    async def getTraits(self):
        return self.traits if self.traits != None or len(self.traits) > 0 else "None"
    
    async def getDescription(self):
        return "{}\n**Damage:** {} - {} {}\n**Crit. Mod**: x{}\nTraits: {}\n".format(
            self.name,
            int(self.base_dmg * (1 - self.variance)),
            int(self.base_dmg * (1 + self.variance)),
            self.dmg_type,
            self.crit_mod,
            ",".join(self.traits if len(self.traits) != 0 else "None")
        ) + await super().getDescription()
    
    async def getStatusDescription(self,STR=0):
        min_dmg = int(self.base_dmg * (1 - self.variance))
        max_dmg = int(self.base_dmg * (1 + self.variance))
        return f"{self.name} | {min_dmg + STR} - {max_dmg + STR} {self.dmg_type} | x{self.crit_mod} Crit. Modifier"

        