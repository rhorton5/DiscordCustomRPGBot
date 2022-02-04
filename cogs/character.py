import discord
from discord.ext import commands
from discord import bot

class Character(commands.Cog):
    def __init__(self,bot):
        self.bot = bot