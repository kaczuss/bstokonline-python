from unittest import TestCase

from app import parse_price


class TestParsePrice(TestCase):
    def test_parse_price_empty(self):
        price = parse_price("")
        self.assertEqual(price, 0)

    def test_parse_price_none(self):
        price = parse_price(None)
        self.assertEqual(price, 0)

    def test_parse_price_simple(self):
        price = parse_price("1999")
        self.assertEqual(price, 1999)

    def test_parse_price_space(self):
        price = parse_price("1 9 99")
        self.assertEqual(price, 1999)

    def test_parse_price_zl(self):
        price = parse_price("1 9 99 zl")
        self.assertEqual(price, 1999)

    def test_parse_price_ZL(self):
        price = parse_price("1 9 99 ZL")
        self.assertEqual(price, 1999)

    def test_parse_price_zly(self):
        price = parse_price("1 9 99 zł")
        self.assertEqual(price, 1999)

    def test_parse_price_wrong_zl(self):
        price = parse_price("1 9 99 zll")
        self.assertEqual(price, 0)

    def test_parse_price_wrong_value(self):
        price = parse_price("19_99")
        self.assertEqual(price, 0)