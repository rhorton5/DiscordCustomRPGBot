from characters.playerCharacter import PlayerCharacter

class Berserker(PlayerCharacter):
    def __init__(self, name: str, STR: int, DEX: int, AGI: int, CON: int, SPR: int, INT: int, WIS: int, CHA: int, LUC: int):
        super().__init__(name, STR, DEX, AGI, CON, SPR, INT, WIS, CHA, LUC)
    
    async def setHP(self):
        self.HP = self.CON + self.SPR + 20
        await super().setHP()
    
    async def setMP(self):
        self.MP = 0
        await super().setMP()
    
    async def getSkillPoints(self):
        return await super().getSkillPoints() + 4
    
    async def getStartingAbilityAmount(self):
        return 4
    
    async def getStartingSpellAmount(self):
        return 0    
    
    async def getClassName(self):
        return "Berserker"