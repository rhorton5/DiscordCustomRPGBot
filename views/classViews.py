from discord.ui import Select, View
from discord import SelectOption, Interaction

class ClassSelection(Select):
    def __init__(self,bot):
        self.bot = bot

        options = [
            SelectOption(label="Mercenary",description="Think Fighter...",emoji="⚔️")
        ]

        super().__init__(
            placeholder="Select your class",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self,interaction: Interaction):
        await interaction.response.send_message(content=f"You have chosen {self.values[0]}")
    
class ClassSelectionView(View):
    def __init__(self,bot):
        super().__init__()
        self.add_item(ClassSelection(bot))
    
    async def getClassSelection(self):
        return self.children[0].values[0]


