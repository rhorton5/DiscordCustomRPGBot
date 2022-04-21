from discord import ApplicationContext
from characters.defaultCharacter import DefaultCharacter
from mechanics.diceRolls import rollD20

async def meleeAttack(ctx: ApplicationContext, attacker: DefaultCharacter, target: DefaultCharacter, rightHand=True):
    atkRoll = rollD20()
    atkScore = await attacker.getMeleeAccuracy() + atkRoll
    armorClass = await target.getArmorClass()
    crits = await attacker.doesCrit(atkRoll)
    responseStr = f"{atkScore} vs AC\n"
    if (atkScore >= armorClass or crits == True) and atkRoll != 1:
        dmg = await attacker.dealMeleeDamage(rightHand,crits)
        dmg = await target.takeDamage(dmg,"Bludgeon")
        responseStr += f"{'**CRITICAL HIT!!!***' if crits == True else ''}\n{await target.getName()} takes {dmg} {'Bludgeon'} damage!"
        await ctx.respond(responseStr)
        return

    responseStr += f"{'***Critical Failure...***' if atkRoll == 1 else ''}\n{await target.getName()} dodged {await attacker.getName()}'s attack."
    await ctx.respond(responseStr)
