from abc import ABC, abstractmethod

from items.item import Item
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
        self.initiative = 0
        self.rHand = None
        self.lHand = None
        self.inventory = list()
    
    def getModifiers(self,att: int):
        return int((att-10)/2)
    
    async def getCarryingCapacity(self):
        return self.STR * 10
    
    async def getArmorClass(self):
        return 10 + self.getModifiers(self.AGI) + self.getModifiers(self.DEX)
    
    async def getMeleeAccuracy(self):
        return self.getModifiers(self.STR)
    
    async def getRangeAccuracy(self):
        return self.getModifers(self.DEX)
    
    async def dealMeleeDamage(self,rightHand=True,crits=False):
        hand = self.rHand if rightHand == True else self.lHand
        return await hand.dealDamage(self.STR if "Finesse" not in await hand.getTraits() else self.DEX,crits)
    
    async def takeDamage(self,dmg,dmgType):
        print(dmg)
        print(dmgType)
        dmgMod = self.elemental_resistance.get(dmgType,0.00) + 1.00
        defenseMod = (self.CON if dmgType in ["Bludgeon","Slash","Pierce"] else self.SPR)
        dmg = int((dmg - defenseMod) * dmgMod)
        if dmg < 0:
            dmg = 0
        self.HP -= dmg
        return dmg
    
    async def isAlive(self):
        return self.HP > 0
    
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
    
    async def doesCrit(self,diceRoll: int):
        return diceRoll >= 20 - int(self.LUC/20)
    
    async def rollInitiative(self,diceRoll=1):
        self.initiative = diceRoll + self.getModifiers(self.AGI)

    def healthDescription(self):
        if self.HP / self.MaxHP == 1.00:
            return "Healthy!"
        elif self.HP / self.MaxHP >= 0.50:
            return "Injured"
        elif self.HP / self.MaxHP >= 0.25:
            return "Really Hurt..."
        elif self.HP > 0:
            return "Critical..."
        else:
            return "KO'ed"
    
    async def sessionStatus(self):
        return f"{self.name}  | Health: **{self.healthDescription()}**"

    
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
        
    async def getName(self):
        return self.name
