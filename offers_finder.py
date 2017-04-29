from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup

class OffersFinder(object):

    def get_latest_offers(self):
        url = 'http://www.bialystokonline.pl/domy-mieszkania-sprzedam,ogloszenia,5,1.html'
        data = urlopen(url).read()
        return self.get_offers(data)

    def get_offers(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        return soup.find_all('div', "ogloszenie")


class OfferParser(object):

    def parse(self, tag):
        offer = Offer()
        offer.premium = "premium" in tag.attrs['class']
        offer.href = tag.div.a['href']
        offer.title = tag.div.a.getText()
        creationData = tag.find('div', 'author')
        offer.addedDate = datetime.strptime(creationData.span.getText()[8:], '%Y-%m-%d %H:%M:%S')
        # tag.find('div','author').span.find_next_sibling('span')
        return offer


class Offer(object):
    pass
