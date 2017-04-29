from mock import mock
from unittest import TestCase

import app_config
from offers_finder import Offer
from storage import OffersStorage


class TestOffersStorage(TestCase):

    @mock.patch('storage.MongoClient')
    @mock.patch('storage.Collation')
    def test_store(self, client, collation):
        offers = list([Offer(), Offer()])
        storage = OffersStorage()
        storage.store(offers)
        # client.assert_called_with(app_config.DB_NAME)

