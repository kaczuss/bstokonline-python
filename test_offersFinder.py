import mock
from unittest import TestCase

from offers_finder import OffersFinder
from datetime import datetime

class TestOffersFinder(TestCase):
    def test_get_offers(self):
        finder = OffersFinder()
        offers = finder.get_offers(open('sample.html', 'r'))
        self.assertEqual(offers.__len__(), 25)

    def side_effect(self, arg):
        values = {'http://www.bialystokonline.pl/domy-mieszkania-sprzedam,ogloszenia,5,1.html': open('sample.html', 'r'),
                 'c': 3}
        return values[arg]


    @mock.patch('offers_finder.urlopen')
    def test_get_latest_offers(self, url_open):
        url_open.side_effect = self.side_effect
        finder = OffersFinder()
        offers = finder.get_latest_offers(datetime.strptime('2017-04-22 12:11:56', '%Y-%m-%d %H:%M:%S'))
        url_open.assert_called_with('http://www.bialystokonline.pl/domy-mieszkania-sprzedam,ogloszenia,5,1.html')
        self.assertEqual(offers.__len__(), 9)



