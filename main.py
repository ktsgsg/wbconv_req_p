#import urllib.parse
import requests
#import json
#import urllib
#from bs4 import BeautifulSoup
#import time
import os
#import sys
import datetime
import webclass
import general


#適当にコメントアウト
"""
defaultpath = "class"
webclassurl = "https://rpwebcls.meijo-u.ac.jp"
def putlog(str):
    STDOUT = sys.stdout
    fp = open("log.txt","a")
    sys.stdout =  fp
    print(str)
    fp.close()
    sys.stdout = STDOUT
    
def getacs(source):
    soup = BeautifulSoup(source,"html.parser")
    exccode = soup.find("script").string
    acsPath = exccode.split('"')[1].replace('&amp;',"&")
    return acsPath

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
        acsPath = getacs(loginphp.text)
        kugiri()
        e = loginphp.cookies.get_dict()
        cookies['WBT_Session'] =e['WBT_Session']
        cookies['SimpleSAML'] = e['SimpleSAML']
        cookies['WCAC'] = e['WCAC']
        print(cookies)
        kugiri()
        webclassurl_ = webclassurl + acsPath
        webclasresponce = requests.get(webclassurl_,cookies=cookies)
        cookies['wcui_session_settings'] = webclasresponce.cookies.get_dict()['wcui_session_settings']
        print(requests.get(webclassurl_,cookies=cookies).headers)
        self.url = webclassurl_
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
    for i in range(10):
        token = requests.post(url,headers=headers,json=jsn)
        statuscode = token.status_code
        #print(statuscode)
        if statuscode == 200:
            break
        time.sleep(0.5)
        
    succesURL = json.loads(token.text)
    tokenId = succesURL["tokenId"]
    #print(succesURL)
    print(f"tokenId:{tokenId}")
    #kugiri()
    return tokenId

def kugiri():
    print("########################################################")

def responceacspath(url,cookies):
    source = requests.get(url,cookies=cookies)
    #print(source.text)
    acspath = getacs(source.text)
    responce = requests.get(webclassurl+acspath,cookies=cookies)
    #print(responce.text)
    return responce

def getcontents(sectionelement:BeautifulSoup,cookies):
    title = sectionelement.find("h4",class_="panel-title").get_text()
    print(f"コース名,{title}")
    putlog(f"コース名,{title}" )

    contentselements = sectionelement.find(class_="list-group").find_all("section",class_="cl-contentsList_listGroupItem")#授業内容のグループを取得
    for j in range(len(contentselements)):
        try:
            contenttitle = contentselements[j].find("h4",class_="cm-contentsList_contentName").find("a")#授業内容のグループのタイトルを取得
            contenturl = contenttitle['href']
            session_qs = urllib.parse.urlparse(contenturl).query#クエリパラメータを取得
            session_qd = urllib.parse.parse_qs(session_qs)#クエリパラメータを辞書型に変換
            contenturl = "https://rpwebcls.meijo-u.ac.jp/webclass/do_contents.php?reset_status=1&"+"set_contents_id="+session_qd["set_contents_id"][0]
            print(f"コンテンツ,{contenttitle.get_text()}")
            #print(f"URL,{contenturl}")
            source = requests.get(contenturl,cookies=cookies)
            acspath = getacs(source.text)
            url = webclassurl+"/webclass/"+acspath
            source = requests.get(url,cookies=cookies)
            soup = BeautifulSoup(source.text,"html.parser")
            putlog(f"content:{contenttitle.get_text()}")
            putlog(f"url:{contenturl}")
            #putlog(f"{source.text}")
            chapterpath = soup.find("frame",{"name":"webclass_chapter"}).attrs["src"].replace("&amp;","&")
            putlog(f"chapterpath:{chapterpath}")
            chapterurl = webclassurl+"/webclass/"+chapterpath
            source_chapter = requests.get(chapterurl,cookies=cookies)
            soup_chapter = BeautifulSoup(source_chapter.text,"html.parser")#チャプターのhtml取得
            #putlog(f"{soup_chapter.prettify}")
            json_str= soup_chapter.find("script",id = "json-data").get_text()
            #putlog(f"str:{json_str}")
            pagedata = json.loads(json_str)#資料の情報をjson形式で保存
            #putlog(json.dumps(pagedata,indent=2))
            text_urls = pagedata["text_urls"]
            for texturl in text_urls.values():
                putlog(f"texturl:{texturl}")
            
        except:
            print("コンテンツ,閉鎖")

def getsections(page,cookies):
    divs = page.find_all("div")  # divタグを持つ要素を取得
    for n in divs:
        n.extract()
    name = page.get_text()
    calssname = name[9:]  # "授業名"の部分を取得
    print(f"授業名:{calssname}")  # 各リンクのURLを表示
    putlog(f"授業名:{calssname}")
    classurl = webclassurl+page['href']
    #print(f"URL:{classurl}")
    os.makedirs(defaultpath+"/"+calssname, exist_ok=True)
    
    source = responceacspath(classurl,cookies)#偽リダイレクトの時のアクセス方法
    soup = BeautifulSoup(source.text,"html.parser")
    sectionelements = soup.find_all("section",class_="cl-contentsList_folder")#授業内容の部分を取得
    for i in range(len(sectionelements)):
        getcontents(sectionelements[i],cookies)
    kugiri()

def getClasses(page,cookies):
    soup = BeautifulSoup(page, "html.parser")

    ##print("ページのHTMLを取得中")

    schedule_element = soup.find(id = "schedule-table")
    hrefs = schedule_element.find_all("a", href=True)
    for href in hrefs:
        getsections(href,cookies)
"""


general.putlog(f"=======================Today:{datetime.datetime.now()},=======================")
general.putlog(f"WBCONV_REQ_P made by ktsgsg.")
os.makedirs(webclass.defaultpath,exist_ok=True)
wbc = webclass.webclass()
source = requests.get(wbc.url,cookies=wbc.cookies)
#putlog(f"requestURL>{wbc.url}")
webclass.getClasses(source.text,wbc.cookies)

