#import urllib.parse
import requests
import json
#import urllib
#from bs4 import BeautifulSoup
#import time
import os
#import sys
import datetime
import webclass
import general
import settings as s


general.putlog(f"=======================Today:{datetime.datetime.now()},=======================")
general.putlog(f"WBCONV_REQ_P made by ktsgsg.")
os.makedirs(webclass.defaultpath,exist_ok=True)
userdata = s.getpsw()
wbc = webclass.webclass(userdata["userid"],userdata["password"])
source = requests.get(wbc.url,cookies=wbc.cookies)
#putlog(f"requestURL>{wbc.url}")
webclass.getClasses(source.text,wbc.cookies)

