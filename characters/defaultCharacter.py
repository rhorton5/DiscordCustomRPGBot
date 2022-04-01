from abc import ABC, abstractmethod
from discord import Embed
class DefaultCharacter(ABC):
    def __init__(self,name: str, STR: int, DEX: int, AGI: int, CON: int, SPR: int, INT: int, WIS: int, CHA: int, LUC: int,img_url = None):
        self.name = name
        self.STR = STR
        self.DEX = DEX
        self.AGI = AGI
        self.CON = CON
        self.SPR = SPR
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.LUC = LUC
        self.HP = 0
        self.MaxHP = 0
        self.MP = 0
        self.MaxMP = 0
        self.img_url = img_url
        self.elemental_resistance = dict()
    
    def getModifiers(self,att: int):
        return int((att-10)/2)
    
    async def getCarryingCapacity(self):
        return self.STR * 5
    
    async def getArmorClass(self):
        return 10 + self.getModifiers(self.AGI) + self.getModifiers(self.DEX)
    
    async def getMeleeAccuracy(self):
        return self.getModifiers(self.STR)
    
    async def getRangeAccuracy(self):
        return self.getModifers(self.DEX)
    
    @abstractmethod
    async def getMagicAccuracy(self):
        pass #This is class dependent
    
    @abstractmethod
    def setHP(self,mod: int):
        pass
    
    @abstractmethod
    def setMP(self, mod: int):
        pass
    
    @abstractmethod
    def getPhysicalAttackPower(self):
        pass
    
    @abstractmethod
    def getMagicalAttackPower(self):
        pass
    
    @abstractmethod
    def getPhysicalDefensePower(self):
        pass

    @abstractmethod
    def getMagicalDefensePower(self):
        pass
    
    async def setSkills(self,skills):
        self.skills = skills
    
    async def getSkillsDict(self):
        return self.skills
    
    async def __getAttribute(self,attribute: str):
        att = {
            "Strength": self.STR,
            "Dexterity": self.DEX,
            "Agility": self.AGI,
            "Constitution": self.CON,
            "Spirit": self.SPR,
            "Intellect": self.INT,
            "Wisdom": self.WIS,
            "Charisma": self.CHA,
            "Luck": self.LUC
        }
        return self.getModifiers(att[attribute])
    
    async def getSkillScoreList(self):
        string = ""
        for skill in self.skills.keys():
            score = self.skills[skill]["Rank Points"] + await self.__getAttribute(self.skills[skill]["Attribute"])
            string += f"**{skill}**: +{score}\n"
        return string
