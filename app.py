import json
import urllib.request as urllib2
import unicodedata
import string

from flask import Flask, render_template, request
from bs4 import BeautifulSoup

app = Flask(__name__)

class RemoveStrangeStuff:

    @staticmethod
    def remove_accents(data):
        return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.printable)

class ScrapeWebsite():

    def __init__(self, url):
        self.url = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        self.ok = True

        try:
            self.page = urllib2.urlopen(url)
        except:
           self.ok = False

@app.route('/getInfo', methods=['POST'])
def getInfo():
    anime_name = request.form['anime_name'];
        
    if (len(anime_name.split(' ')) > 1):
        anime_name = '-'.join(anime_name.lower().split(' '))

    scraper = ScrapeWebsite(f"https://wall.alphacoders.com/search.php?search={anime_name}")

    if(scraper.ok): 
        soup = BeautifulSoup(scraper.page, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'boxgrid'})
        imgs = []

        for idx, div in enumerate(divs):
            imgs.append(RemoveStrangeStuff.remove_accents(div.find('img')['src']))

    return json.dumps({'status':'OK', 'imgs': imgs});

@app.route("/")
def index():
    return render_template('index.html')
 
if __name__ == "__main__":
    app.debug = True
    app.run()