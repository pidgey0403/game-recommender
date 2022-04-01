from unicodedata import name
from bs4 import BeautifulSoup
import requests

def scraper(query):
   r = requests.get('https://en.wikipedia.org/wiki/'+query)
   soup = BeautifulSoup(r.content,'html.parser')
   covers = soup.select('table.infobox a.image img[src]')
   for cover in covers:
         print('https:'+cover['src'])

title = "The_Legend_of_Zelda:_Breath_of_the_Wild"
