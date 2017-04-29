from datetime import datetime

from bs4 import BeautifulSoup
from unittest import TestCase

from offers_finder import OfferParser


class TestOfferParser(TestCase):
    def test_parse_ogloszenie_premium(self):
        parser = OfferParser()
        offer = parser.parse(BeautifulSoup(open("ogloszenie_premium.html", "r"), 'html.parser').div)
        self.assertIsNotNone(offer)
        self.assertTrue(offer.premium)
        self.assertEqual(offer.href, "http://www.bialystokonline.pl/polecamy-dom-murowany-wolnostojacy-na-osiedlu-dojlidy-gorne,ogloszenie,4169506,5,1.html")
        self.assertEqual(offer.title, "Polecamy dom murowany, wolnostojący na osiedlu Dojlidy Górne.")
        self.assertEqual(offer.addedDate, datetime.strptime('2017-04-22 09:17:44', '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(offer.id, '4169506')

    def test_parse_ogloszenie_zwykle(self):
        parser = OfferParser()
        offer = parser.parse(BeautifulSoup(open("ogloszenie_zwykle.html", "r"), 'html.parser').div)
        self.assertIsNotNone(offer)
        self.assertFalse(offer.premium)
        self.assertEqual(offer.href, "http://www.bialystokonline.pl/dom-wolnostojacy-65m2-dzialka-980m2-tyniewicze-male-163-tys-zl,ogloszenie,4169790,5,1.html")
        self.assertEqual(offer.title, "** Dom wolnostojący 65m2, działka 980m2, Tyniewicze Małe, 163 tyś.zł **")
        self.assertEqual(offer.addedDate, datetime.strptime('2017-04-22 19:29:23', '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(offer.id, '4169790')
