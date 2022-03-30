from abc import ABC, abstractmethod
from characters.defaultCharacter import DefaultCharacter

class PlayerCharacter(DefaultCharacter,ABC):
    def __init__(self,name: str, STR: int, DEX: int, AGI: int, CON: int, SPR: int, INT: int, WIS: int, CHA: int, LUC: int):
        super().__init__(name,STR,DEX,AGI,CON,SPR,INT,WIS,CHA,LUC)
        self.level = 1
        self.xp = 0
        
    async def setHP(self, mod: int):
        self.MaxHP = self.HP
    
    #Override if the class is a spellcaster type
    async def setMP(self, mod: int):
        self.MaxMP = self.MP
    
    async def addXP(self,xp: int):
        self.xp += xp
        if self.xp <= self.__getNextLevel():
            self.level += 1
            return True
        return False
    
    def __getNextLevel(self):
        return 150 * pow(self.level * 5,2)
    
    def getAttackPower(self):
        return self.STR + 10
    
    def getDefensePower(self):
        return self.CON
    
    async def __getLevelMod(self):
        return int(self.level/3) + 1
    
    async def getMeleeAccuracy(self):
        return await super().getMeleeAccuracy() + self.__getLevelMod()
    
    async def getMagicAccuracy(self):
        return self.getModifiers(self.INT) + self.__getLevelMod()
    
    async def getRangeAccuracy(self):
        return await super().getRangeAccuracy() + self.__getLevelMod()
        
    
