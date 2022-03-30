from abc import ABC, abstractmethod
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
    
    def getModifiers(self,att: int):
        return int((att-10)/2)
    
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
