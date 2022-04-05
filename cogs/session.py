from pydoc import describe
from discord import Bot, Cog, Embed, slash_command
from jsons.jsonManager import loadCharacterJson
from characters.loadCharacter import loadCharacter

#Colors
normal_emb_color = 0x0096FF
combat_emb_color = 0xFF5733 


class Session(Cog):
    def __init__(self,bot) -> None:
        super().__init__()
        self.bot = bot
        self.activeSession = dict()
    
    @slash_command(name="start_session",description="Starts the session for this campaign!",guild_ids=[903338023960313876])
    async def startSession(self,ctx):
        guild_id = str(ctx.guild.id)
        if(self.activeSession.get(guild_id,None) == None):
            self.activeSession[guild_id] = dict()
            self.activeSession[guild_id]["Characters"] = list()
            self.activeSession[guild_id]["ChannelMSG"] = await ctx.respond(embed=await self.__createSessionEmbed(guild_id))
        else:
            await ctx.respond("You already have a session")
    
    async def __createSessionEmbed(self,guild_id: str):
        emb = Embed(title="The Campaign!",description="",color=normal_emb_color)
        if len(self.activeSession[guild_id]["Characters"]) == 0:
            emb.add_field(name="Characters",value="Add Characters with the /add command",inline=False)
        else:
            emb.add_field(name="Characters",value="\n".join(
                [await char.sessionStatus() for char in self.activeSession[guild_id]["Characters"]]
                )
            )
        return emb
    
    async def __createEndSessionEmbed(self):
        emb = Embed(title="Your Session Has Ended!",description="If you want to start it up again, use the /start_session command!",color=normal_emb_color)
        return emb
    
    @slash_command(name="add_character",description="Add your character to the session",guild_ids=[903338023960313876])
    async def addCharacter(self,ctx,character_name: str):
        guild_id = str(ctx.guild.id)
        if(self.activeSession.get(guild_id,None) == None): #Can I make this into a check?
            await ctx.respond("You need to start a session first!")
        else:
            charJson = loadCharacterJson()
            author_id = str(ctx.author.id)
            if(charJson.get(author_id,None) == None):
                await ctx.respond("You do not have a character made!")
            else:
                if(charJson[author_id].get(character_name,None)) == None:
                    await ctx.respond(f"{character_name} was not found.")
                else:
                    cJson = charJson[author_id][character_name]
                    self.activeSession[guild_id]["Characters"].append(await loadCharacter(character_name,cJson))
                    await self.activeSession[guild_id]["ChannelMSG"].edit_original_message(embed=await self.__createSessionEmbed(guild_id))
                    await ctx.respond(f"{character_name} has been added!!")
    
    @slash_command(name="end_session",description="End the session",guild_ids=[903338023960313876])
    async def endSession(self,ctx):
        guild_id = str(ctx.guild.id)
        if(self.activeSession.get(guild_id,None) == None):
            await ctx.respond("You don't have a session active currently.")
        else:
            await self.activeSession[guild_id]["ChannelMSG"].edit_original_message(embed=await self.__createEndSessionEmbed())
            self.activeSession.pop(guild_id)
            await ctx.respond("The session has ended!")

def setup(bot: Bot):
    bot.add_cog(Session(bot))
    

