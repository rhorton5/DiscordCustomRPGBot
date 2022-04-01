from discord.ui import Select, View, Button
from discord import Embed, SelectOption, Interaction
from discord import ButtonStyle
from jsons.jsonManager import getSkillList

class FirstLevelSkill(Select):
    def __init__(self,bot,skills,skillpoints=0):
        self.bot = bot
        options = list()

        #There is over 25 skills, need to figure out a way to disperse all of them and add all the skills together.
        for s in skills.keys():
            if skills[s].get("Subtypes",None) == None:
                options.append(SelectOption(label=s,description=skills[s]["Attribute"]))

        super().__init__(
            placeholder = "Select your skills",
            min_values = 1,
            max_values = skillpoints,
            options = options
        )
    
    async def callback(self,interaction: Interaction):
        await interaction.response.send_message(content=f"Skills have been chosen!")

class SubtypeFirstLevelSkills(Select):
    def __init__(self,bot,skills,skillpoints=0):
        self.bot = bot
        options = list()
        for s in skills.keys():
            if skills[s].get("Subtypes",None) != None:
                for type in skills[s]["Subtypes"]:
                    options.append(
                        SelectOption(label=f"{s} [{type}]",description=skills[s]["Attribute"])
                    )

        super().__init__(
            placeholder = "Select your subtype of your skills",
            min_values = 1,
            max_values = skillpoints,
            options = options
        )

    async def callback(self,interaction: Interaction):
        await interaction.response.send_message(content=f"Subtypes have been chosen!")


class SkillConfirmationButton(Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.primary,label="Confirm Skills!")
    
    async def callback(self,interaction: Interaction):
        interaction.response.is_done()
        self.disabled = True


class FirstLevelSkillView(View):
    def __init__(self,bot,skillpoints=0):
        super().__init__()
        self.skills = getSkillList()
        self.skillpoints = skillpoints
        self.add_item(FirstLevelSkill(bot,self.skills,skillpoints))
        self.add_item(SubtypeFirstLevelSkills(bot,self.skills,skillpoints))
        self.add_item(SkillConfirmationButton())
    
    async def getEmbeddedMessage(self):
        return Embed(title="Select your skills",description=f"Skills are broken up by main types and subtypes, so be sure to look at both of them!\nYou can use **{self.skillpoints}** skills!")

    async def getSkillSelections(self):
        skillList = self.children[0].values + self.children[1].values
        print(skillList)
        res = dict()
        for s in skillList:
            chosenSkill = self.skills.get(s,None)
            if chosenSkill == None:
                skillName = s[:s.index(' ')].strip()
                chosenSkillDict = {
                    "Attribute": self.skills[skillName]["Attribute"],
                    "Rank Points": 1
                }
                res[s] = chosenSkillDict
            else:
                chosenSkill["Rank Points"] = 1
                res[s] = chosenSkill
        return res
    
    def buttonPressed(self):
        return len(self.children[0].values + self.children[1].values) == self.skillpoints