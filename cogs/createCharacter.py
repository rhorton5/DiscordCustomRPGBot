import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import ApplicationContext, SelectOption, Embed
from json import load

guildID = [903338023960313876]
class CreateCharacter(commands.Cog):
    def __init__(self,bot: discord.Bot):
        self.bot = bot
        print("Character has been created!")
    
    @commands.slash_command(name="create_character",guild_ids=guildID)
    async def createCharacter(self,ctx: ApplicationContext):
        attributes = {"Strength": 10, "Dexterity": 10, "Agility": 10, "Constitution": 10,"Resistance": 10,
                        "Intellect": 10, "Wisdom": 10, "Charisma": 10, "Luck": 10}
        
        def createCharacterSheet(attributes):
            characterSheetEmb = Embed(title="Character Attribute")

            characterSheetEmb.add_field(name="Dervied Attributes",value="HP: {0} / {0}\nMP: {1} / {1}\nLP: {2} / {2}".format(
                attributes["Constitution"] + attributes["Resistance"], 0, int((attributes["Luck"]-10)/2)
            ),
            inline=False)

            characterSheetEmb.add_field(name="Attribute Score",value="\n".join(
            [f"{att}: {attributes[att]} [{int((attributes[att] - 10)/2)}]" for att in attributes.keys()]
            ),
            inline=False)

            characterSheetEmb.add_field(name="Offensive/Defensive Attributes",
            value="Armor Class: {}\nMagic Attack Score: {}\nMelee Attack Score: {}\nRanged Attack Score: {}".format(
                int((attributes['Dexterity']-10)/2) + int((attributes['Agility']-10)/2) + 10,
                0,
                int((attributes['Strength']-10)/2) + 1,
                int((attributes['Dexterity']-10)/2) + 1
            ))
            return characterSheetEmb
        
        def checkAttributeScore(m: discord.Message):
            try:
                score = int(m.content)
                return score >= 8 and score <= 20
            except Exception:
                return False

        emb = createCharacterSheet(attributes)
        embMsg = await ctx.send(embed=emb)
        '''for attributeScores in attributes.keys():
            msg = await ctx.send(f"Enter your {attributeScores} score.")
            attributes[attributeScores] =  int((await self.bot.wait_for("message",check=checkAttributeScore,timeout=120.0)).content)
            await msg.delete()
            emb = createCharacterSheet(attributes)
            await embMsg.edit(embed=emb)'''
        await self.selectClass(ctx,emb,attributes,embMsg)

    async def updateEmbedWithSelectedClass(self,attributes: dict,selectedClass: dict):
        print(selectedClass)
        characterSheetEmb = Embed(title="Character Attribute")

        if "Alchemist" in selectedClass.keys():
            selectedClass["Starting MP"] = int((attributes[selectedClass["Starting MP"]]-10)/2) * 2
        elif selectedClass["Starting MP"] == None:
            selectedClass["Starting MP"] = 0
        else:
            selectedClass["Starting MP"] = int((attributes["Wisdom"]-10)/2)

        characterSheetEmb.add_field(name="Dervied Attributes",value="HP: {0} / {0}\nMP: {1} / {1}\nLP: {2} / {2}".format(
            attributes["Constitution"] + attributes["Resistance"] + selectedClass["Starting HP"], 
            selectedClass["Starting MP"],    
            int((attributes["Luck"]-10)/2)
        ),
        inline=False)

        characterSheetEmb.add_field(name="Attribute Score",value="\n".join(
        [f"{att}: {attributes[att]} [{int((attributes[att] - 10)/2)}]" for att in attributes.keys()]
        ),
        inline=False)

        magicAttackScore = int((selectedClass["Starting MP"]-10)/2) if "Alchemist" not in selectedClass.keys() else int(selectedClass["Starting MP"]/2)
        characterSheetEmb.add_field(name="Offensive/Defensive Attributes",
        value="Armor Class: {}\nMagic Attack Score: {}\nMelee Attack Score: {}\nRanged Attack Score: {}".format(
            int((attributes['Dexterity']-10)/2) + int((attributes['Agility']-10)/2) + 10,
             magicAttackScore,
            int((attributes['Strength']-10)/2) + 1,
            int((attributes['Dexterity']-10)/2) + 1
        ))
        return characterSheetEmb


            


        
        

def setup(bot: discord.Bot):
    bot.add_cog(CreateCharacter(bot))
