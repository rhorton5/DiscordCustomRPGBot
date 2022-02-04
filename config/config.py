from json import load

def GetToken(testToken = False):
    with open("botConfig.json",'r') as dataFile:
        jsonData = load(dataFile)
        if(testToken == True):
            return jsonData['test_token']
        else:
            return jsonData['token']

