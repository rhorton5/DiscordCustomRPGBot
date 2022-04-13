from items.weapon import Weapon
from items.armor import Armor
from items.item import Item

def createItem(name: str, itemDict: dict):
    print(f"Creating {name}!")
    if itemDict["Type"] == "Weapon":
        return Weapon(name,itemDict["Value"],itemDict["Weight"],itemDict["Base Damage"],itemDict["Damage Type"],itemDict["Critical Modifier"],itemDict["Variance"],itemDict["Traits"])
     
    return Item(name,itemDict["Value"],itemDict["Weight"])