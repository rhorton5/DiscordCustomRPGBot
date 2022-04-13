from characters.playerCharacter import PlayerCharacter
from discord import Embed
class CharacterSheetEmb():
    async def createCharacterSheet(self,character: PlayerCharacter):
        emb = Embed(title=f"{await character.getName()}'s Status",description=f"A Level {character.level} {await character.getClassName()}")
        emb.add_field(name="Attributes",value=await character.createStatsSheet(),inline=True)
        emb.add_field(name="Elemental Resistance",value=await character.createElementalResistanceSheet(),inline=True)
        emb.add_field(name="Equipment",value=await character.createEquipmentStatus(),inline=False)
        emb.add_field(name="Inventory Info",value=await character.createInventoryStatus(),inline=False)
        emb.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/800px-Question_mark_%28black%29.svg.png")
        return emb
