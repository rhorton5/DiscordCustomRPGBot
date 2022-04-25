from pydoc import describe
from discord import ApplicationCommand, ApplicationContext, Bot, Cog, Embed, slash_command
from characters.defaultCharacter import DefaultCharacter
from items.item import Item
from jsons.jsonManager import loadCharacterJson, loadWeaponJson
from characters.loadCharacter import loadCharacter
from views.characterSheetEmb import CharacterSheetEmb
from items.itemFactory import createItem
from mechanics.combat import meleeAttack, startInitiative

#Colors
normal_emb_color = 0x0096FF
combat_emb_color = 0xFF5733 


class Session(Cog):
    def __init__(self,bot) -> None:
        super().__init__()
        self.bot = bot
        self.activeSession = dict()
        tmpItem = loadWeaponJson()
        self.items = [createItem(i,tmpItem[i]) for i in tmpItem.keys()]
        print(self.items) 
    
    @slash_command(name="start_session",description="Starts the session for this campaign!",guild_ids=[903338023960313876])
    async def startSession(self,ctx):
        await self.createSessionEmbed(ctx)
    
    @slash_command(name="add_character",description="Add your character to the session",guild_ids=[903338023960313876])
    async def addCharacter(self,ctx,character_name: str):
        guild_id = str(ctx.guild.id)
        if(self.activeSession.get(guild_id,None) == None): #Can I make this into a check?
            await self.createSessionEmbed(ctx)
        charJson = loadCharacterJson()
        author_id = str(ctx.author.id)
        if(charJson.get(author_id,None) == None):
            await ctx.respond("You do not have a character made!")
        else:
            if(charJson[author_id].get(character_name,None)) == None:
                await ctx.respond(f"{character_name} was not found.")
            else:
                cJson = charJson[author_id][character_name]
                c = await loadCharacter(character_name,cJson)
                await c.setAuthorID(author_id)
                self.activeSession[guild_id]["Characters"].append(c)
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
    
    @slash_command(name="status",description="Shows the select character's status",guild_ids=[903338023960313876])
    async def status(self,ctx: ApplicationContext,name:str):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if await self.isActiveSession(guild_id) == False:
            await ctx.respond("You must have an active session first...")
            return
        
        character = await self.getCharacter(guild_id,name)
        if character == None:
            await ctx.respond("Your character does not exist in this session...")
            return
        
        cse = CharacterSheetEmb()
        await ctx.respond(embed=await cse.createCharacterSheet(character))
    
    @slash_command(name="inspect_item",description="Describes an item either in your inventory or currently in the session.",guild_ids=[903338023960313876])
    async def inspect(self,ctx: ApplicationContext, item_name: str):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if await self.isActiveSession(guild_id) == False:
            await ctx.respond("You must have an active session first...")
            return

        itemList = list(filter(lambda i: i.getName() == item_name, self.activeSession[guild_id]["Items"]))
        #TO-DO: Add a function to inspect a character.
        
        for i in itemList:
            await ctx.send(embed=await self.__createItemDescription(i))
        await ctx.respond("These are the items found...")   
    
    async def getItemFromStash(self,guild_id: str,item_name: str):
        return list(filter(lambda i: i.getName() == item_name,self.activeSession[guild_id]["Items"]))
    
    @slash_command(name="grab_item",description="Take an item to your character's inventory",guild_ids=[903338023960313876])
    async def grabItem(self,ctx: ApplicationContext, character_name: str, item_name: str):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if await self.isActiveSession(guild_id) == False:
            await ctx.respond("You must have an active session first...")
            return
        
        character = await self.getCharacter(guild_id,character_name)
        if character == None or await character.getAuthorID() != author_id:
            await ctx.respond("Your character does not exist in this session...")
            return
        
        filterItemList = await self.getItemFromStash(guild_id,item_name)
        if len(filterItemList) == 0:
            await ctx.respond("The item was not found")
        else:
            await character.addItem(filterItemList[0])
            await ctx.respond(f"{await character.getName()} has added {filterItemList[0].getName()} to their inventory!")
            await self.removeItemFromItemsList(guild_id,filterItemList)
            await self.activeSession[guild_id]["ChannelMSG"].edit_original_message(embed=await self.__createSessionEmbed(guild_id))
    
    @slash_command(name="equip_to_hand",description="Equip an item to your hand",guild_ids=[903338023960313876])
    async def equipToHand(self,ctx: ApplicationContext,character_name: str, itemname: str, righthand: bool):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if await self.isActiveSession(guild_id) == False:
            await ctx.respond("You must have an active session first...")
            return
        
        character = await self.getCharacter(guild_id,character_name)
        if character == None or await character.getAuthorID() != author_id:
            await ctx.respond("Your character does not exist in this session...")
            return
        
        item = await character.getItem(itemname)
        if len(item) > 0 and item[0] != None:
            await self.addItemToCharactersHand(ctx,character,item,righthand)
        else:
            item = await self.getItemFromStash(guild_id,itemname)
            if len(item) == 0:
                await ctx.respond("You do not have this item...")
            else:
                await self.addItemToCharactersHand(ctx,character,item,righthand)
                await self.removeItemFromItemsList(guild_id,item)
                await self.activeSession[guild_id]["ChannelMSG"].edit_original_message(embed=await self.__createSessionEmbed(guild_id))
    
    @slash_command(name="unequip_from_hand",description="Remove an item from your hand back to your inventory.",guild_ids=[903338023960313876])
    async def unequipFromHand(self,ctx: ApplicationContext,character_name:str,righthand: bool):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if await self.isActiveSession(guild_id) == False:
            await ctx.respond("You must have an active session first...")
            return
        
        character = await self.getCharacter(guild_id,character_name)
        if character == None or await character.getAuthorID() != author_id:
            await ctx.respond("Your character does not exist in this session...")
            return
        
        await character.unequipHand(righthand)
        await ctx.respond("Removed from hand.")
    
    @slash_command(name="melee_attack",description="Attack a character",guild_ids=[903338023960313876])
    async def attack(self,ctx: ApplicationContext,attacker_name:str, target_name:str,right_hand: bool):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if await self.isActiveSession(guild_id) == False:
            await ctx.respond("You must have an active session first...")
            return
        
        attacker_character = await self.getCharacter(guild_id,attacker_name)
        target_character = await self.getCharacter(guild_id,target_name)
        if attacker_character == None or target_character == None:
            await ctx.respond("Your character does not exist in this session...")
            return
        
        await meleeAttack(ctx,attacker_character,target_character,right_hand)
        await self.activeSession[guild_id]["ChannelMSG"].edit_original_message(embed=await self.__createSessionEmbed(guild_id))
    
    @slash_command(name="start_encounter",description="Start an encounter",guild_ids=[903338023960313876])
    async def startEncounter(self,ctx: ApplicationContext):
        guild_id = str(ctx.guild.id)
        if await self.isActiveSession(guild_id) == False:
            await ctx.respond("You must have an active session first...")
            return
        
        self.activeSession[guild_id]["Characters"] = await startInitiative(self.activeSession[guild_id]["Characters"])
        self.activeSession[guild_id]["Combat"] = True
        await self.activeSession[guild_id]["ChannelMSG"].edit_original_message(embed=await self.__createSessionEmbed(guild_id)) 
        await ctx.respond("The encounter has started!  It is {}'s turn!".format(await self.activeSession[guild_id]["Characters"][0].getName()))
    
    @slash_command(name="next_turn",description="Move turns",guild_ids=[903338023960313876])
    async def nextTurn(self,ctx):
        guild_id = str(ctx.guild.id)
        if await self.isActiveSession(guild_id) == False:
            await ctx.respond("You must have an active session first...")
            return
        
        #Change Character Turns
        c = self.activeSession[guild_id]["Characters"].pop(0)
        self.activeSession[guild_id]["Characters"].append(c)

        #Update Channel Embed
        await self.activeSession[guild_id]["ChannelMSG"].edit_original_message(embed=await self.__createSessionEmbed(guild_id)) 
        
        #Notify of Player's turn
        await self.sendCharacterTurn(ctx,guild_id)

             
    #Commonly Used Methods
    async def removeItemFromItemsList(self,guild_id: str, itemList: list):
        self.activeSession[guild_id]["Items"].remove(itemList[0])
    
    async def __createItemDescription(self,item: Item):
        return Embed(title=item.getName(),description=await item.getDescription())

    async def __createEndSessionEmbed(self):
        emb = Embed(title="Your Session Has Ended!",description="If you want to start it up again, use the /start_session command!",color=normal_emb_color)
        return emb
    
    async def getCharacter(self,guild_id:str, name:str):
        characterList = self.activeSession[guild_id]["Characters"]
        for c in characterList:
            if await c.getName() == name:
                return c
        return None
    
    async def isActiveSession(self,guild_id:str):
        return self.activeSession.get(guild_id,None) != None
        
    async def __createSessionEmbed(self,guild_id: str):
        emb = Embed(title="The Campaign!",description=self.activeSession[guild_id]["Description"],color=normal_emb_color if self.activeSession[guild_id]["Combat"] == False else combat_emb_color)
        if len(self.activeSession[guild_id]["Characters"]) == 0:
            emb.add_field(name="Characters",value="Add Characters with the /add_character command",inline=False)
        else:
            inCombat = self.activeSession[guild_id]["Combat"]
            emb.add_field(name="Characters",value="\n".join(
                [await char.sessionStatus(inCombat) for char in self.activeSession[guild_id]["Characters"]]
                ),
                inline=False
            )
        if len(self.activeSession[guild_id]["Items"]) != 0:
            emb.add_field(name="Items",value=" | ".join(
                    [i.getName() for i in self.activeSession[guild_id]["Items"]]
                ),
                inline=False
            )
        return emb  
    
    async def createSessionEmbed(self,ctx: ApplicationContext):
        guild_id = str(ctx.guild.id)
        if(self.activeSession.get(guild_id,None) == None):
            self.activeSession[guild_id] = dict()
            self.activeSession[guild_id] = {
                "Characters": list(),
                "Items": self.items,
                "Description": "A normal adventure",
                "ChannelMSG": None,
                "Combat": False
            }
            print(self.activeSession[guild_id])
            self.activeSession[guild_id]["ChannelMSG"] = await ctx.respond(embed=await self.__createSessionEmbed(guild_id))
        else:
            await ctx.respond("You already have a session")
    
    async def addItemToCharactersHand(self,ctx: ApplicationContext, character: DefaultCharacter, item: list, righthand: bool):
        await character.removeItem(item[0].getName())
        await character.equipToHand(item[0],righthand)
        await ctx.respond(f"{item[0].getName()} has been added to {await character.getName()}'s {'Right' if righthand == True else 'Left'} Hand")
    
    async def sendCharacterTurn(self,ctx: ApplicationContext, guild_id: str):
        await ctx.respond("It is {}'s turn!".format(await self.activeSession[guild_id]["Characters"][0].getName()))

def setup(bot: Bot):
    bot.add_cog(Session(bot))
    