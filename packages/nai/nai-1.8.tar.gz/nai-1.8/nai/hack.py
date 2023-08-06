from requests import *
from bs4 import *
from colours import *

def phonesearch(numb):
   num = str(numb)
   if len(num) != 10:
    if "0" in num:
     num = num[1:]
    elif "+92" in num:
     num = num.split("+92")[1]
   url = "https://simdatabaseonline.com/tele/search.php?num={}"
   try:
     html = BeautifulSoup(get(url.format(num)).content,"html.parser")
     data = html.find("table")
     print(W+"-"*3+Y+"NEXDataBase-Records"+W+"-"*3)
     for x in data.find_all("tr"):
       try:
         print(G+x.get_text())
       except: pass
     print(W+"-"*10)
   except:
     if data != None:
      print(R+"ERROR : Network Error !")
     elif data == None:
      print(R+"ERROR : NOT FOUND !")
 