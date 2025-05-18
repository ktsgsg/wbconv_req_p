import urllib
import urllib.parse
import requests
import webclass
import general as g

def get_fileurl(query_str):
    query = urllib.parse.parse_qs(query_str)
    result = []
    contents_url = query["contents_url"]
    file = query["file"]
    if ".pdf" in file[0]:
        result.append("pdf")
    else:
        result.append("other")
    #print(contents_url,file)
    fileurl = webclass.webclassurl + contents_url[0] + file[0]
    result.append(fileurl)#要素0にはファイルのタイプ 1にはファイルのurl
    return result
    
def downloadpdf(url,cookies,filepath):
    source = requests.get(url,cookies=cookies)
    pdfdata = source.content
    file = open(filepath,"wb")
    file.write(pdfdata)
    file.close()

def getfiles(query,cookies,filepath):
    fileurl = get_fileurl(query)
    print(fileurl)
    if fileurl[0] == "pdf":
        print("Filetype:PDF")
        print(f"Downloading:{fileurl[1]} to {filepath}")
        downloadpdf(fileurl[1],cookies,filepath)
        print("done.")
        g.putlog(f"filepath:{filepath}")
    else:
        print("The file is in a format that cannot be downloaded.")

"""
query = "/webclass/txtbk_show_text.php?page=1&text=7e1580301496d50b522dffc68c6a4d21&file=442a35021a1283f1bfcc4d600706e16d%2Fbfcc4d600706e16d.pdf&contents_dir=%2Fvar%2Fwww%2Fwebclass%2Ftext%2F20%2F2025016424080%2F&contents_url=%2Fwebclass%2Ftext%2F20%2F2025016424080%2F&contents_id=e19bc32431943c0cd5814fe40b44be91"
url = "https://www.mext.go.jp/component/b_menu/shingi/toushin/__icsFiles/afieldfile/2015/02/13/1355038_9.pdf"
wb = webclass.webclass()
getfiles(query,wb.cookies,"test.pdf")
"""