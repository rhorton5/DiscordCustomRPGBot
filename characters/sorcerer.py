from characters.playerCharacter import PlayerCharacter
from items.item import Item
class Sorcerer(PlayerCharacter):
    def __init__(self,name: str, STR: int, DEX: int, AGI: int, CON: int, SPR: int, INT: int, WIS: int, CHA: int, LUC: int):
        super().__init__(name,STR,DEX,AGI,CON,SPR,INT,WIS,CHA,LUC)
        
    async def setHP(self):
        self.HP = self.CON + self.SPR + 5
        await super().setHP()
    
    async def setMP(self):
        self.MP = self.getModifiers(self.WIS)
        await super().setMP()
    
    async def getSkillPoints(self):
        return await super().getSkillPoints() + 2
    
    async def getStartingAbilityAmount(self):
        return 2
    
    async def getStartingSpellAmount(self):
        return 2
    
    async def getClassName(self):
        return "Sorcerer"
    
    async def __getClassLevelMod__(self):
        return int(self.level/3) + 1