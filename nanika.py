from bs4 import BeautifulSoup as b

with open("source.text","r") as f:
    t = f.read()

soup = b(t,"html.parser")
with open("index.html","w") as f:
    f.write(soup.prettify())