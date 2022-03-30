from discord import Bot, Cog, slash_command
from characters.alchemist import Alchemist
from characters.mercenary import Mercenary
from views.characterSheetView import CharacterSheetView
from views.classViews import ClassSelectionView

class CreateCharacter(Cog):
    def __init__(self,bot: Bot):
        self.bot = bot
    
    @slash_command(name="create_character",description="Create a new character to use later",guild_ids=[903338023960313876])
    async def createCharacter(self,ctx):
        await ctx.respond("You will make your character in the DMs")
        dm = ctx.author.dm_channel
        if dm == None:
            await ctx.author.create_dm()
            dm = ctx.author.dm_channel
        attributeScores = await self.__getCharacterAttributes(dm,ctx.author.name)
        playerClass = await self.__selectClass(dm)
        pc = await PlayerCharacterFactory.createCharacter(attributeScores["Name"],attributeScores,playerClass)
        csv = CharacterSheetView(pc)
        await ctx.send(embed=await csv.createEmbed())
    
    async def __getCharacterAttributes(self,dm,author_name):
        #Checks
        def nameCheck(m):
            return m.author.name == author_name
            
        def checkAttributeScore(m):
            try:
                att = int(m.content)
                return att <= 20 and att > 8
            except Exception:
                    return False
            
        #Get Name
        await dm.send("Enter your character's name: ")
        name = (await self.bot.wait_for('message',check=nameCheck)).content
            
        #Get Attributes
        attDict = {"Strength": 0, "Dexterity": 0, "Agility": 0, "Constitution": 0, "Spirit": 0, "Intellect": 0, "Wisdom": 0, "Charisma": 0, "Luck": 0}
        for att in attDict.keys():
            await dm.send(f"What is {name}'s {att}?")
            attScore = int((await self.bot.wait_for('message',check=checkAttributeScore)).content)
            attDict[att] = attScore
            
        attDict["Name"] = name
        return attDict
    
    async def __selectClass(self,dm):
        csv = ClassSelectionView(self.bot)
        def hasChosenClass(i):
            return True
        await dm.send(view=csv)
        await self.bot.wait_for('interaction',check=hasChosenClass)
        return await csv.getClassSelection()
        

class PlayerCharacterFactory:
    async def createCharacter(name: str, att: dict, className: str):
        switch = {
            "Mercenary": Mercenary,
            "Alchemist": Alchemist
        }
        pc = switch[className](name,att["Strength"],att["Dexterity"],att["Agility"],att["Constitution"],att["Spirit"],att["Intellect"],att["Wisdom"],att["Charisma"],att["Luck"])
        await pc.setHP()
        await pc.setMP()
        await pc.setLP()
        return pc

def setup(bot: Bot):
    bot.add_cog(CreateCharacter(bot))
