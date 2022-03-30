from discord import Embed
from characters.playerCharacter import PlayerCharacter

class CharacterSheetView():
    def __init__(self,char: PlayerCharacter) -> None:
        self.char = char
    
    async def createEmbed(self):
        e = Embed(title=f"{self.char.name}'s Status",type="rich")
        e.add_field(name="Attributes",value=await self.char.createStatsSheet(),inline=False)
        e.add_field(name="Damage Resistance",value=await self.char.createElementalResistanceSheet(),inline=False)
        return e
