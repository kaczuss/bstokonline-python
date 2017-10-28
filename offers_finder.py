import importlib
from datetime import datetime
from urllib.request import urlopen

import os
from bs4 import BeautifulSoup

app_config = importlib.import_module('app_config_{}'.format(os.getenv('bstok_env')))

max_pages = getattr(app_config, 'MAX_PAGES', 6)


class OffersFinder(object):
    def __init__(self) -> None:
        self.offers_parser = OfferParser()

    def get_latest_offers(self, since):
        all_offers = list()
        for i in range(1, max_pages):
            url = 'http://www.bialystokonline.pl/domy-mieszkania-sprzedam,ogloszenia,5,{}.html'.format(i)
            data = urlopen(url).read()
            offers = self.get_offers(data)
            filtered = list(filter(lambda o: o.creation_date > since, offers))
            all_offers.extend(filtered)
            if filtered.__len__() < offers.__len__():
                break

        return sorted(all_offers, key=lambda offer: offer.creation_date)

    def get_offers(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        tags = soup.find_all('div', 'ogloszenie')
        tags = filter(lambda t: 'google_ad_client' not in t.getText(), tags)
        return list(map(lambda t: self.offers_parser.parse(t), tags))


class OfferParser(object):
    def parse(self, tag):
        offer = Offer()
        offer.premium = "premium" in tag.attrs['class']
        offer.url = "http://www.bialystokonline.pl/" + tag.div.a['href']
        offer.description = tag.find('div', "content").getText()
        offer.title = tag.div.a.getText()
        creation_data = tag.find('div', 'author')
        offer.creation_date = datetime.strptime(creation_data.span.getText()[8:], '%Y-%m-%d %H:%M:%S')
        offer._id = creation_data.span.find_next_sibling('span').getText()[3:]
        user_data = creation_data.span.find_next_sibling('span').find_next_sibling('span')
        if user_data is not None:
            offer.user = creation_data.span.find_next_sibling('span').find_next_sibling('span').getText()[12:]
        else:
            offer.user = None
        price_tag = tag.find('div', 'price')
        if price_tag is not None:
            offer.price = price_tag.span.getText()
        else:
            offer.price = None

        url_tag = tag.find('div', 'url')
        if url_tag is not None:
            offer.extra_url = url_tag.a['href']
        else:
            offer.extra_url = None

        return offer


class Offer(object):
    pass
