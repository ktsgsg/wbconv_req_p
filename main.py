import requests
import json

def getToken():
    url = 'https://slbsso.meijo-u.ac.jp/opensso/json/authenticate' 
    
    headers = {
        'Content-Type' : 'application/json'
    }
    str = requests.post(url,headers=headers)
    jsn = json.loads(str.text)
    jsn["callbacks"][0]["input"][0]["value"] = '241205181'
    jsn["callbacks"][1]["input"][0]["value"] = 'Yamake2011$'
    file = open("data.json","w")
    json.dump(jsn,file,indent=2)
    file.close()
    token = requests.post(url,headers=headers,json=jsn)
    succesURL = json.loads(token.text)
    tokenId = succesURL["tokenId"]
    #print(f"tokenId:{tokenId}")
    return tokenId
    
    
def getWebclass():
    headers = {
        'Content-Type' : 'application/json'
    }
    tokenId = getToken()
    url = "https://rpwebcls.meijo-u.ac.jp/webclass/login.php?auth_mode=SAML"
    req = requests.get(url,allow_redirects=False)
    dicts =req.cookies.get_dict()
    dicts["iPlanetDirectoryPro"]=tokenId
    req2=requests.post(url,headers=headers,cookies=dicts,allow_redirects=False)
    print(req2.status_code)
getWebclass()

