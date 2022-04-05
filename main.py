from discord import bot
from jsons.jsonManager import getTokenKey


bot = bot.Bot()

@bot.event
async def on_ready():
    print("Bot is ready to go!")

bot.load_extension('cogs.utility')
bot.load_extension('cogs.character')
bot.load_extension('cogs.session')

bot.run(getTokenKey())

