from discord import ApplicationContext
from characters.defaultCharacter import DefaultCharacter
from mechanics.diceRolls import rollD20

async def skillCheck(c: DefaultCharacter,skillName: str,attribute: str):
    diceRoll = rollD20()
    print(f"Dice Roll is ... {diceRoll}")
    crits = await c.doesCrit(diceRoll)
    fails = False
    skillMod = await c.getSkillMod(skillName,attribute)
    totalScore = diceRoll + skillMod
    return {"Score": totalScore, "Crits": crits, "Fails": fails, "hasSkill": skillMod != 0}