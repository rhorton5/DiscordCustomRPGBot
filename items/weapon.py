from items.item import Item
class Weapon(Item):
    def __init__(self, name: str, value: int, weight: float,base_dmg: int, dmg_type: str, crit_mod: float,traits: list) -> None:
        super().__init__(name, value, weight)
        self.base_dmg = base_dmg
        self.dmg_type = dmg_type
        self.crit_mod = crit_mod
        self.traits = traits
    
    async def getType(self):
        return "Weapon"
    
    async def getBaseDamage(self):
        return self.base_dmg
    
    async def getCriticalModifier(self):
        return self.crit_mod

    async def getTraits(self):
        return self.traits if self.traits != None or len(self.traits) > 0 else "None"

        