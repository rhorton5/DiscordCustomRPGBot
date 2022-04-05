from discord import Bot, Cog, Embed, slash_command
from jsons.jsonManager import loadCharacterJson

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
            self.activeSession[guild_id]["ChannelMSG"] = await ctx.respond(embed=await self.__createSessionEmbed())
        else:
            await ctx.respond("You already have a session")
    
    async def __createSessionEmbed(self):
        emb = Embed(title="The Campaign!",description="",color=normal_emb_color)
        emb.add_field(name="Characters",value="Add Characters with the /add command",inline=False)
        return emb



def setup(bot: Bot):
    bot.add_cog(Session(bot))
    

