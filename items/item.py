from abc import ABC, abstractmethod
class Item(ABC):
    def __init__(self,name: str, value: int, weight: float) -> None:
        self.name = name
        self.value = value
        self.weight = weight
    
    def getName(self):
        return self.name
    
    async def getValue(self):
        return self.value
    
    async def getWeight(self):
        return self.weight
    
    @abstractmethod
    async def getType(self):
        pass

    async def getDescription(self):
        return "**Weight:** {} lbs.\nValue: {} Gold".format(self.weight,self.value)