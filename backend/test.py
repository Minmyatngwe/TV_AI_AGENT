from bs4 import BeautifulSoup
import re 
import requests
response=requests.get("https://www.roboai.fi/uutinen/roboai-roadshow-taytti-euran-urheilutalon-teknologialla-katso-kuvat/")

soup=BeautifulSoup(response.content,'html.parser')
text=soup.text
text_clean=re.sub(r"\n+","\n",text)

images = soup.select('div[class*="fl-photo-img-"]')
for div in images:
    a_tag = div.find("a")
    if a_tag:
        print(a_tag["href"])