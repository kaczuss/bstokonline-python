from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup


class OffersFinder(object):
    def __init__(self) -> None:
        self.offers_parser = OfferParser()

    def get_latest_offers(self, since):
        all_offers = list()
        for i in range(1, 6):
            url = 'http://www.bialystokonline.pl/domy-mieszkania-sprzedam,ogloszenia,5,{}.html'.format(i)
            data = urlopen(url).read()
            offers = self.get_offers(data)
            filtered = list(filter(lambda o: o.creationDate > since, offers))
            all_offers.extend(filtered)
            if filtered.__len__() < offers.__len__():
                return all_offers

        return all_offers

    def get_offers(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        tags = soup.find_all('div', 'ogloszenie')
        tags = filter(lambda t: 'google_ad_client' not in t.getText(), tags)
        return list(map(lambda t: self.offers_parser.parse(t), tags))


class OfferParser(object):
    def parse(self, tag):
        offer = Offer()
        offer.premium = "premium" in tag.attrs['class']
        offer.href = tag.div.a['href']
        offer.title = tag.div.a.getText()
        creation_data = tag.find('div', 'author')
        offer.creationDate = datetime.strptime(creation_data.span.getText()[8:], '%Y-%m-%d %H:%M:%S')
        offer.id = creation_data.span.find_next_sibling('span').getText()[3:]
        user_data = creation_data.span.find_next_sibling('span').find_next_sibling('span')
        if user_data is not None:
            offer.user = creation_data.span.find_next_sibling('span').find_next_sibling('span').getText()[12:]
        else:
            offer.user = None

        return offer


class Offer(object):
    pass
