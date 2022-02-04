import discord

bot = discord.Bot()

def GetGuildIds():
    return [903338023960313876]

@bot.check
async def IsInGuild(ctx):
    return ctx.guild.id in GetGuildIds()

@bot.slash_command(name="hello",guild_ids=GetGuildIds())
async def hello(ctx, name="hello"):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")

@bot.slash_command(name="add",guild_ids=GetGuildIds())
async def add(ctx,a: int, b: int):
    await ctx.respond(f"{a + b}")


@bot.slash_command(name="button",guild_ids=GetGuildIds())
async def button(ctx):

    async def button1Callback(interaction: discord.Interaction):
        return await interaction.response.send_message("You've pressed button 1")
    
    async def button2Callback(interaction: discord.Interaction):
        return await interaction.response.send_message("You've pressed button 2")
    
    v = discord.ui.View()
    button = discord.ui.Button(label="Test",style=discord.ButtonStyle.primary)
    button2 = discord.ui.Button(label="This is my second button",style=discord.ButtonStyle.danger)
    button.callback = button1Callback
    button2.callback = button2Callback

    v.add_item(button)
    v.add_item(button2)
    await ctx.send("This is a test",view=v)



@bot.user_command(name="Say Hello")
async def hi(ctx, user):
    await ctx.respond(f"{ctx.author.mention} says hello to {user.name}!")

@bot.event
async def on_ready():
    print(f"Bot is operation!")


print("Loading Cogs")
bot.load_extension('cogs.utility')
bot.load_extension('cogs.createCharacter')


bot.run("OTA5ODU4NTc3OTg3MDM5MzAy.YZKZ1Q.giQ6s1Ta5fkg3VawIcgxBOGvy94")