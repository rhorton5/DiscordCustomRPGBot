from abc import ABC, abstractmethod
from characters.defaultCharacter import DefaultCharacter

class PlayerCharacter(DefaultCharacter,ABC):
    def __init__(self,name: str, STR: int, DEX: int, AGI: int, CON: int, SPR: int, INT: int, WIS: int, CHA: int, LUC: int):
        super().__init__(name,STR,DEX,AGI,CON,SPR,INT,WIS,CHA,LUC)
        self.level = 1
        self.xp = 0
        self.ele_res = dict()
        
    async def setHP(self):
        self.MaxHP = self.HP
    
    #Override if the class is a spellcaster type
    async def setMP(self):
        self.MaxMP = self.MP
    
    async def setLP(self):
        self.LP = self.getModifiers(self.LUC)
        self.MaxLP = self.LP
    
    async def addXP(self,xp: int):
        self.xp += xp
        if self.xp <= self.__getNextLevel():
            self.level += 1
            return True
        return False
    
    async def __getNextLevel(self):
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
    
    async def getMagicalAttackPower(self):
        return 0
    
    async def getMagicalDefensePower(self):
        return 0
    
    async def getPhysicalAttackPower(self):
        return 0
    
    async def getPhysicalDefensePower(self):
        return 0
    
    async def createStatsSheet(self):
        return "❤️ **HP**: {}/{}\n✨ **MP**: {}/{}\n🍀 **LP**: {}/{}\n\n**XP**: {:,}/{:,}\n\n**Strength**: {}\n**Dexterity**: {}\n**Agility**: {}\n**Constitution**: {}\n**Spirit**: {}\n**Intellect**: {}\n**Wisdom**: {}\n**Charisma**: {}\n**Luck**: {}".format(
            self.HP,self.MaxHP,self.MP,self.MaxMP,self.LP,self.MaxLP,self.xp,await self.__getNextLevel(),self.STR,self.DEX,self.AGI,self.CON,self.SPR,self.INT,self.WIS,self.CHA,self.LUC
        )
    
    async def createElementalResistanceSheet(self):
        return "🔥 Fire: {}% | 🌊 Water: {}% | 🌱 Earth: {}%\n💨 Wind: {}% | 🧊 Ice: {}% | ☠️ Posion: {}%\n☢️ Acid: {}% | ⚡ Electric: {}% | 💡 Light: {}%\n🌙 Dark: {}% | 👁️ Psychic: {}% | 🟣 Slag: {}%\n✊ Bludgeon: {}% | 📌 Pierce: {}% | 🗡️ Slash: {}%".format(
            1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
        )

        
    
