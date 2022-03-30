from characters.playerCharacter import PlayerCharacter
class Mercenary(PlayerCharacter):
    def __init__(self,name: str, STR: int, DEX: int, AGI: int, CON: int, SPR: int, INT: int, WIS: int, CHA: int, LUC: int):
        super().__init__(name,STR,DEX,AGI,CON,SPR,INT,WIS,CHA,LUC)
        
    async def setHP(self):
        self.HP = self.CON + self.SPR + 10
        super().setHP()
    
    async def setMP(self):
        self.MP = self.getModifiers(self.INT)
        super().setMP()