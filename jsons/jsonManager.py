from json import load, dump

def getSkillList():
    with open("jsons/skillList.json","r") as skillListJson:
        return load(skillListJson)
    
def saveCharacterJson(char):
    with open("jsons/characterJson.json","w") as characterJson:
        dump(char,characterJson,indent=2,sort_keys=True)

def loadCharacterJson():
    with open("jsons/characterJson.json","r") as characterJson:
        return load(characterJson)

def getTokenKey():
    with open("jsons/config.json","r") as config:
        return load(config)["Token"]