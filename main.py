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


general.putlog(f"=======================Today:{datetime.datetime.now()},=======================")
general.putlog(f"WBCONV_REQ_P made by ktsgsg.")
os.makedirs(webclass.defaultpath,exist_ok=True)
wbc = webclass.webclass()
source = requests.get(wbc.url,cookies=wbc.cookies)
#putlog(f"requestURL>{wbc.url}")
webclass.getClasses(source.text,wbc.cookies)

