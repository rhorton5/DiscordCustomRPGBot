from discord import Embed, ButtonStyle, Interaction
from discord.ui import View, Button
from characters.playerCharacter import PlayerCharacter

class CharacterSheetView():
    def __init__(self,char: PlayerCharacter) -> None:
        self.char = char
    
    async def createEmbed(self):
        e = Embed(title=f"{self.char.name}'s Status",type="rich")
        e.add_field(name="Attributes",value=await self.char.createStatsSheet(),inline=False)
        e.add_field(name="Damage Resistance",value=await self.char.createElementalResistanceSheet(),inline=False)
        e.add_field(name="Skills",value=await self.char.getSkillScoreList(),inline=False)
        return e

class ConfirmButton(Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.success,label="Yes!")
        self.pressed = False
    
    async def callback(self, interaction: Interaction):
        print("Confirming!")
        self.pressed = True
        return interaction.response.is_done()
    
class CancelButton(Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.success,label="No!")
        self.pressed = False
    
    async def callback(self, interaction: Interaction):
        self.pressed = True
        return interaction.response.is_done()


class ConfirmStats(View):
    def __init__(self):
        super().__init__()
        self.add_item(ConfirmButton())
        self.add_item(CancelButton())
    
    def buttonPressed(self):
        res = self.children[0].pressed == True or self.children[1].pressed == True
        print(res)
        return res
    
    async def getResult(self):
        return True if self.children[0].pressed == True else False
    


