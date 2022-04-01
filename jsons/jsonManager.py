from json import load, dump

def getSkillList():
    with open("jsons/skillList.json","r") as skillListJson:
        return load(skillListJson)
    
def saveCharacterJson(char):
    with open("jsons/characterJson.json","w") as characterJson:
        dump(char,characterJson,indent=2,sort_keys=True)