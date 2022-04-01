from discord import bot
from sys import argv


bot = bot.Bot()

@bot.event
async def on_ready():
    print("Bot is ready to go!")

bot.load_extension('cogs.utility')
bot.load_extension('cogs.character')

if len(argv) <= 0:
    print("Please supply a key to use!!")
else:
  bot.run(argv[1])

