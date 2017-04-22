from unittest import TestCase

from offers_finder import OffersFinder


class TestOffersFinder(TestCase):
    def test_get_offers(self):
        finder = OffersFinder()
        offers = finder.get_offers(open('sample.html', 'r'))
        self.assertEqual(offers.__len__(), 27)
