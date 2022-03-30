from discord import ApplicationContext, slash_command
from discord.ext.commands import Cog, Bot
from discord.ext import commands

from characters.mercenary import Mercenary

class Utility(Cog):
    def __init__(self,bot: Bot):
        self.bot = bot
    
    @slash_command(name="ping",description="Ping to make sure this bot is alive!",guild_ids=[903338023960313876])
    async def ping(self,ctx: ApplicationContext):
        await ctx.respond(f"Pong!  Your latency is {round(self.bot.latency * 100,2)} miliseconds!")   

def setup(bot: Bot):
    bot.add_cog(Utility(bot))