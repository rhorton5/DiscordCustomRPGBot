from abc import ABC, abstractmethod
from characters.defaultCharacter import DefaultCharacter
from items.armor import Armor
from items.item import Item
from items.weapon import Weapon

class PlayerCharacter(DefaultCharacter,ABC):
    def __init__(self,name: str, STR: int, DEX: int, AGI: int, CON: int, SPR: int, INT: int, WIS: int, CHA: int, LUC: int):
        super().__init__(name,STR,DEX,AGI,CON,SPR,INT,WIS,CHA,LUC)
        self.level = 1
        self.xp = 0
        self.ele_res = dict()
        self.rHand = None
        self.lHand = None
        self.armor = None
        self.accesories = list()
        
    async def configureCharacter(self,jsonStats: dict):
        attributes = jsonStats["Attributes"][0]
        self.HP = attributes["HP"]
        self.MaxHP = attributes["MaxHP"]
        self.MP = attributes["MP"]
        self.MaxMP = attributes["MaxMP"]
        self.xp = attributes["XP"]
        self.level = attributes["Level"]
        self.id = jsonStats["AuthorID"]
        self.gold = jsonStats["Gold"]
        self.ele_res = jsonStats["Resistance"]

        self.skills = jsonStats["Skills"]
        await self.setLP()
    
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
    
    @abstractmethod
    def __getClassLevelMod__(self):
        pass
    
    async def getMeleeAccuracy(self):
        return await super().getMeleeAccuracy() + self.__getLevelMod()
    
    async def getMagicAccuracy(self):
        return self.getModifiers(self.INT) + self.__getLevelMod()
    
    async def getRangeAccuracy(self):
        return await super().getRangeAccuracy() + self.__getLevelMod()
    
    async def getMagicalAttackPower(self):
        return self.INT
    
    async def getMagicalDefensePower(self):
        score = self.SPR
        if self.armor != None:
            score += await self.armor.getMagicalDefense()
        return score
    
    async def getPhysicalAttackPower(self):
        wpn = self.rHand if self.rHand != None else self.lHand
        if wpn == None:
            return self.STR + 10
        else:
            return await wpn.getBaseDamage() + self.STR
    
    async def getPhysicalDefensePower(self):
        score = self.CON
        if self.armor != None:
            score += await self.armor.getPhysicalDefense()
        return score
        
    
    async def createStatsSheet(self):
        return "❤️ **HP**: {}/{}\n✨ **MP**: {}/{}\n🍀 **LP**: {}/{}\n\n**XP**: {:,}/{:,}\n\n**Strength**: {}\n**Dexterity**: {}\n**Agility**: {}\n**Constitution**: {}\n**Spirit**: {}\n**Intellect**: {}\n**Wisdom**: {}\n**Charisma**: {}\n**Luck**: {}".format(
            self.HP,self.MaxHP,self.MP,self.MaxMP,self.LP,self.MaxLP,self.xp,await self.__getNextLevel(),self.STR,self.DEX,self.AGI,self.CON,self.SPR,self.INT,self.WIS,self.CHA,self.LUC
        )
    
    async def createElementalResistanceSheet(self):
        return "🔥 Fire: {}% \n 🌊 Water: {}% \n 🌱 Earth: {}%\n💨 Wind: {}% \n 🧊 Ice: {}% \n ☠️ Poison: {}%\n☢️ Acid: {}% \n ⚡ Electric: {}% \n 💡 Light: {}%\n🌙 Dark: {}% \n 👁️ Psychic: {}% \n 🟣 Slag: {}%\n✊ Bludgeon: {}% \n 📌 Pierce: {}% \n 🗡️ Slash: {}%".format(
            *[
                self.ele_res.get(ele,0) for ele in
                ["Fire","Water","Earth","Wind","Ice","Poison","Acid","Electric","Light","Dark","Psychic","Slag","Bludgeon","Pierce","Slash"]
            ]
        )
    
    async def createEquipmentStatus(self):
        rhandDesc = await self.rHand.getStatusDescription(self.STR) if self.rHand != None else "-" * 10
        lHandDesc = await self.lHand.getStatusDescription(self.STR) if self.lHand != None else "-" * 10
        armorDesc = await self.armor.getStatusDescription() if self.armor != None else "-" * 10

        return "Right Hand: {}\nLeft Hand: {}\n\nArmor: {}".format(rhandDesc,lHandDesc,armorDesc)
    
    async def createInventoryStatus(self):
        return "Gold: {}\nInventory Weight: {} lbs. / {} lbs.".format(
            self.gold, 
            sum([await i.getWeight() for i in self.inventory]), 
            await self.getCarryingCapacity()
            )
    
    async def getSkillPoints(self):
        return self.getModifiers(self.INT)
    
    async def addItem(self,item: Item):
        self.inventory.append(item)
    
    async def removeItem(self,itemName: str):
        itemMatches = list(filter(lambda i: i.getName() == itemName,self.inventory))
        if len(itemMatches) == 0:
            return False
        self.inventory.remove(itemMatches[0]) #just remove the first instance
        return True

    
    @abstractmethod
    async def getStartingAbilityAmount(self):
        pass
    
    @abstractmethod
    async def getStartingSpellAmount(self):
        pass
    
    @abstractmethod
    async def getClassName(self):
        pass
    
    async def sessionStatus(self):
        return f"{self.name}  | Lvl. {self.level} | Health: **{self.healthDescription()}**"
    
    async def setAuthorID(self,author_id:str):
        self.id = author_id
    
    async def getAuthorID(self):
        return self.id
    
    async def generateJson(self):
        json = dict()
        json["Attributes"] = {
            "Level": self.level,
            "XP": self.xp,
            "HP": self.HP,
            "MaxHP": self.MaxHP,
            "MP": self.MP,
            "MaxMP": self.MaxMP,
            "Strength": self.STR, 
            "Dexterity": self.DEX, 
            "Agility": self.AGI,
            "Constitution": self.CON,
            "Spirit": self.SPR,
            "Intellect": self.INT,
            "Wisdom": self.WIS,
            "Charisma": self.CHA,
            "Luck": self.LUC,
            "LP": self.LP,
            "MaxLP": self.MaxLP
        },
        json["Equipment"] = {
            "Right Hand": None,
            "Left Hand": None,
            "Accessories": [],
            "Armor": None
        },
        json["Inventory"] = [],
        json["Gold"] = 150,
        json["Spells"] = {},
        json["Abilities"] = {},
        json["Skills"] = await self.getSkillsDict()
        json["Resistance"] = {}
        json["Class"] = await self.getClassName()
        json["AuthorID"] = await self.getAuthorID()
        return json
        
    
