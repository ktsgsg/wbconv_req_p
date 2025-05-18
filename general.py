import sys

def putlog(str):
    STDOUT = sys.stdout
    fp = open("log.txt","a")
    sys.stdout =  fp
    print(str)
    fp.close()
    sys.stdout = STDOUT

def kugiri():
    print("########################################################")
