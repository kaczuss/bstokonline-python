from bs4 import BeautifulSoup

class OffersFinder(object):

    def get_offers(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        return soup.find_all('div', "ogloszenie")


class OfferParser(object):

    def parse(self, tag):
        offer = Offer()
        print(tag.attrs)
        offer.premium = "premium" in tag.attrs['class']
        return offer


class Offer(object):
    pass
