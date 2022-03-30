from items.item import Item
class Armor(Item):
    def __init__(self, name: str, value: int, weight: float, phys_res: int, magi_res: int, ele_res: dict) -> None:
        super().__init__(name, value, weight)
        self.phys_res = phys_res
        self.magi_res = magi_res
        self.ele_res = ele_res
    
    async def getType(self):
        return "Armor"
    
    async def getPhysicalDefense(self):
        return self.phys_res
    
    async def getMagicalDefense(self):
        return self.magi_res
    
    async def getElementalResistance(self,element: str):
        return self.ele_res.get(element.lower(),0.00)

