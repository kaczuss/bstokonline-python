from bs4 import BeautifulSoup
from unittest import TestCase

from offers_finder import OfferParser


class TestOfferParser(TestCase):
    def test_parse_ogloszenie_premium(self):
        parser = OfferParser()
        offer = parser.parse(BeautifulSoup(open("ogloszenie_premium.html", "r"), 'html.parser').div)
        self.assertIsNotNone(offer)
        self.assertTrue(offer.premium)

    def test_parse_ogloszenie_zwykle(self):
        parser = OfferParser()
        offer = parser.parse(BeautifulSoup(open("ogloszenie_zwykle.html", "r"), 'html.parser').div)
        self.assertIsNotNone(offer)
        self.assertFalse(offer.premium)
