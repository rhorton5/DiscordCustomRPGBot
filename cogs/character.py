from discord import Bot, Cog, Embed, slash_command
from characters.alchemist import Alchemist
from characters.berserker import Berserker
from characters.mercenary import Mercenary
from characters.playerCharacter import PlayerCharacter
from views.characterSheetView import CharacterSheetView, ConfirmStats
from views.classViews import ClassSelectionView
from views.firstLevelSkillView import FirstLevelSkillView
from jsons.jsonManager import loadCharacterJson, saveCharacterJson

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
        skills = await self.__selectSkills(dm,pc)
        await pc.setSkills(skills)
        if await self.__confirmChoice(dm,pc) == True:
            await dm.send(f"Your character has been saved!!")
            json = loadCharacterJson()
            if json.get(str(ctx.author.id),None) == None:
                json[str(ctx.author.id)] = dict()
            json[str(ctx.author.id)][await pc.getName()] = await pc.generateJson()
            saveCharacterJson(json)
            
        else:
            await CreateCharacter(ctx)

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
    
    async def __selectSkills(self,dm,pc: PlayerCharacter):
        flsv = FirstLevelSkillView(self.bot,await pc.getSkillPoints())

        def hasChosenSkills(i):
            return flsv.buttonPressed()

        await dm.send(view=flsv,embed=await flsv.getEmbeddedMessage())
        await self.bot.wait_for('interaction',check=hasChosenSkills)
        return await flsv.getSkillSelections()

    async def __confirmChoice(self,dm,pc: PlayerCharacter):
        csv = CharacterSheetView(pc)
        cs = ConfirmStats()
        
        def confirmButtonPressed(i):
            return True
        
        await dm.send(view=cs,embed=await csv.createEmbed())
        await  self.bot.wait_for('interaction',check=confirmButtonPressed)

        return await cs.getResult()

class PlayerCharacterFactory:
    async def createCharacter(name: str, att: dict, className: str):
        switch = {
            "Mercenary": Mercenary,
            "Alchemist": Alchemist,
            "Berserker": Berserker
        }
        pc = switch[className](name,att["Strength"],att["Dexterity"],att["Agility"],att["Constitution"],att["Spirit"],att["Intellect"],att["Wisdom"],att["Charisma"],att["Luck"])
        await pc.setHP()
        await pc.setMP()
        await pc.setLP()
        return pc

def setup(bot: Bot):
    bot.add_cog(CreateCharacter(bot))
