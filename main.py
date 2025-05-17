import urllib.parse
import requests
import json
import urllib
from bs4 import BeautifulSoup
import time
import os

defaultpath = "class"

class webclass:
    def __init__(self):
        tokenId = getToken()
        url = "https://rpwebcls.meijo-u.ac.jp/webclass/login.php?auth_mode=SAML"
        res = requests.get(url,allow_redirects=False)
        #print("location")
        #print(res.headers)
        #kugiri()
        location = res.headers["Location"]
        cookies = res.cookies.get_dict()
        cookies["iPlanetDirectoryPro"]= tokenId
        #print("cookies:")
        #print(cookies)
        #kugiri()

        wbres = requests.get(location,cookies=cookies)
        #print(wbres.text)
        #kugiri()
        soup = BeautifulSoup( wbres.text,"html.parser")
        responsedatas =soup.find_all("input")
        SAMLResponse=responsedatas[0].attrs["value"]
        RelayState = responsedatas[1].attrs["value"]
        data = {
            "SAMLResponse" :SAMLResponse,
            "RelayState":RelayState
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        req = urllib.parse.urlencode(data)
        defaultsp = "https://rpwebcls.meijo-u.ac.jp/simplesaml/module.php/saml/sp/saml2-acs.php/default-sp"
        wbres = requests.post(defaultsp,cookies=cookies,headers=headers,data=req,allow_redirects=False)
        #print(data)
        kugiri()
        print("SAMLAuthToken")
        SimpleSAML = wbres.cookies.get_dict()['SimpleSAML']
        SimpleSAMLAuthToken = wbres.cookies.get_dict()['SimpleSAMLAuthToken']
        cookies['SimpleSAML'] = SimpleSAML
        cookies['SimpleSAMLAuthToken'] = SimpleSAMLAuthToken
        print(cookies)
        kugiri()
        loginphp = requests.get(url,cookies=cookies,allow_redirects=False)
        soup = BeautifulSoup(loginphp.text,"html.parser")
        exccode = soup.find("script").string
        acsPath = exccode.split('"')[1]
        print(acsPath)
        kugiri()
        e = loginphp.cookies.get_dict()
        cookies['WBT_Session'] =e['WBT_Session']
        cookies['SimpleSAML'] = e['SimpleSAML']
        cookies['WCAC'] = e['WCAC']
        print(cookies)
        kugiri()
        webclassurl = "https://rpwebcls.meijo-u.ac.jp" + acsPath
        webclasresponce = requests.get(webclassurl,cookies=cookies)
        cookies['wcui_session_settings'] = webclasresponce.cookies.get_dict()['wcui_session_settings']
        print(requests.get(webclassurl,cookies=cookies).headers)
        self.url = webclassurl
        self.cookies = cookies

def getToken():
    url = 'https://slbsso.meijo-u.ac.jp/opensso/json/authenticate?realm=/enduser&realm=/' \
    'enduser&forward=true&spEntityID=https%3A%2F%2Frpwebcls.meijo-u.ac.jp%2Fsaml-sp&goto=/' \
    'opensso%2FSSORedirect%2FmetaAlias%2Fenduser%2Fidp6%3FReqID%3D_b59b5741fd497f353186a827' \
    '3aa2e30628f083f316%26index%3Dnull%26acsURL%3Dhttps%253A%252F%252Frpwebcls.meijo-u.ac.jp%' \
    '252Fsimplesaml%252Fmodule.php%252Fsaml%252Fsp%252Fsaml2-acs.php%252Fdefault-sp%26spEntit' \
    'yID%3Dhttps%253A%252F%252Frpwebcls.meijo-u.ac.jp%252Fsaml-sp%26binding%3Durn%253Aoasis%2' \
    '53Anames%253Atc%253ASAML%253A2.0%253Abindings%253AHTTP-POST&AMAuthCookie=' 
    
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
    statuscode = 0
    while(statuscode != 200):
        token = requests.post(url,headers=headers,json=jsn)
        statuscode = token.status_code
        #print(statuscode)
        time.sleep(0.5)
    succesURL = json.loads(token.text)
    tokenId = succesURL["tokenId"]
    #print(succesURL)
    print(f"tokenId:{tokenId}")
    #kugiri()
    return tokenId
def kugiri():
    print("########################################################")

def getClasses(page):
    soup = BeautifulSoup(page, "html.parser")

    ##print("ページのHTMLを取得中")

    schedule_element = soup.find(id = "schedule-table")
    hrefs = schedule_element.find_all("a", href=True)
    for href in hrefs:
        divs = href.find_all("div")  # divタグを持つ要素を取得
        for n in divs:
            n.extract()
        name = href.get_text()
        calssname = name[9:]  # "授業名"の部分を取得
        print(f"NAME:{calssname}")  # 各リンクのURLを表示
        print(f"URL:{"https://rpwebcls.meijo-u.ac.jp"+href['href']}")
        os.makedirs(defaultpath+"/"+calssname, exist_ok=True)

os.makedirs(defaultpath,exist_ok=True)
wbc = webclass()
source = requests.get(wbc.url,cookies=wbc.cookies).text
getClasses(source)

