from json import load

def getSkillList():
    with open("jsons/skillList.json","r") as skillListJson:
        return load(skillListJson)