from characters.alchemist import Alchemist
from characters.berserker import Berserker
from characters.mercenary import Mercenary
from characters.playerCharacter import PlayerCharacter
async def loadCharacter(name: str,charJson: dict):
    class_name = charJson["Class"]
    
    switch = {
        "Mercenary": Mercenary,
        "Alchemist": Alchemist,
        "Berserker": Berserker
    }

    attributes = charJson["Attributes"][0]
    STR = attributes["Strength"]
    DEX = attributes["Dexterity"]
    AGI = attributes["Agility"]
    CON = attributes["Constitution"]
    SPR = attributes["Spirit"]
    INT = attributes["Intellect"]
    WIS = attributes["Wisdom"]
    CHA = attributes["Charisma"]
    LUC = attributes["Luck"]

    char = switch.get(class_name,Mercenary)(name,STR,DEX,AGI,CON,SPR,INT,WIS,CHA,LUC)
    await char.configureCharacter(charJson)
    return char