from discord import bot

bot = bot.Bot()

@bot.event
async def on_ready():
    print("Bot is ready to go!")

bot.load_extension('cogs.utility')
bot.load_extension('cogs.character')

bot.run("OTA5ODU4NTc3OTg3MDM5MzAy.YZKZ1Q.tOc-GTSG55Ymbld5aOavBa-g46k")

