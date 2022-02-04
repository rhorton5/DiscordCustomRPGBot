from discord.ext.commands import cog
from discord.ext import commands
from discord import Bot, Cog

class Utility(Cog):
    def __init__(self,client: Bot):
        self.client = client
        print("Utility has been added")
    
    

def setup(client: Bot):
    client.add_cog(Utility(client))