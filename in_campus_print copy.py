import urllib.parse
import requests
import json
import urllib
from bs4 import BeautifulSoup as b
import time
import os
import general as g
import filedownload
import webclass
import settings as s
import io
from multipart import MultipartParser

def get_MRH():
    userdata = s.getpsw()
    token = webclass.getToken(userdata["userid"],userdata["password"])
    ipurl = "https://ccmoon2.meijo-u.ac.jp/f5-w-68747470733a2f2f63636470737276312e6d65696a6f2d752e61632e6a70$$/user/f5-h-$$/user/f5-h-$$/user/f5-h-$$/api/system/notice/ownipaddress"
    token_cookie = {
        "iPlanetDirectoryPro" : token,
    }
    source = requests.get("https://ccmoon2.meijo-u.ac.jp/",cookies=token_cookie,allow_redirects=False)
    soup = b(source.text,"html.parser")
    g.kugiri()
    printerCookie = dict(**token_cookie,**source.cookies.get_dict())
    
    headers = {
        "Content-Type" : "application/json;charset=UTF-8"
    }
    source = requests.get(ipurl,cookies= printerCookie)
    print(source.text)
    
    fileDataBinary = open("test.pdf", 'rb').read()
    headers = {
        "Content-Type" : "multipart/form-data; boundary=----geckoformboundaryf419f29ef302bfbe5311d10501528a6"
    }
    boundary = "----geckoformboundaryf419f29ef302bfbe5311d10501528a6"
    jsn = {"user_id":"241205181","queue_id":"web-ondemand","ip":"192.168.230.231","paper_type":"06","duplex_type":"1","color_mode_type":"1","copies":"1","number_up":"1","orientation_edge":"1","print_orientation":"2","page_sort":"1"}
    data = {'json': json.dumps(jsn)}
    
    payload = (
        f"Content-Disposition: form-data; name=\"data\"; filename=\"blob\"\r\n"
        f"Content-Type: application/json\r\n\r\n"
        
        f"{data}\r\n"
        f"{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"UNUGA\"; filename=\"file.pdf\"\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{fileDataBinary.decode('utf-8')}\r\n"
        f"{boundary}\r\n"
    )
    

get_MRH()