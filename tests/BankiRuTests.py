import unittest
import random

from apis.BankiRu import BankiRu
from apis.BankiRu import BankiRuError
from apis.BankiRu import parser_HTML
from apis.BankiRu import str_to_float


class BankiRuTests(unittest.TestCase):
    def test_parser_HTML_is_not_none(self):
        self.assertIsNotNone(parser_HTML('usd', 'moskva'))

    def test_parser_HTML_Error(self):
        with self.assertRaises(BankiRuError):
            parser_HTML('vgbhnjm', 'vgbhnjmk')

    def test_str_to_float(self):
        number = random.random()
        self.assertEqual(number, str_to_float(f'{number}'))

    def test_get_rate_bank_name_type_1(self):
        bank_1 = BankiRu('usd', 'moskva')
        for bank_key, bank_value in bank_1.get_rate().items():
            self.assertTrue(isinstance(bank_key, str))

    def test_get_rate_curr_name_type_1(self):
        bank_1 = BankiRu('usd', 'moskva')
        for bank_key, bank_value in bank_1.get_rate().items():
            self.assertTrue(isinstance(bank_value.name_currency, str))

    def test_get_rate_rate_buy_type_1(self):
        bank_1 = BankiRu('usd', 'moskva')
        for bank_key, bank_value in bank_1.get_rate().items():
            self.assertTrue(isinstance(bank_value.rate_buy, float))

    def test_get_rate_rate_sell_type_1(self):
        bank_1 = BankiRu('usd', 'moskva')
        for bank_key, bank_value in bank_1.get_rate().items():
            self.assertTrue(isinstance(bank_value.rate_sell, float))

    def test_get_rate_bank_name_type_2(self):
        bank_2 = BankiRu('eur', 'moskva')
        for bank_key, bank_value in bank_2.get_rate().items():
            self.assertTrue(isinstance(bank_key, str))

    def test_get_rate_curr_name_type_2(self):
        bank_2 = BankiRu('eur', 'moskva')
        for bank_key, bank_value in bank_2.get_rate().items():
            self.assertTrue(isinstance(bank_value.name_currency, str))

    def test_get_rate_rate_buy_type_2(self):
        bank_2 = BankiRu('eur', 'moskva')
        for bank_key, bank_value in bank_2.get_rate().items():
            self.assertTrue(isinstance(bank_value.rate_buy, float))

    def test_get_rate_rate_sell_type_2(self):
        bank_2 = BankiRu('eur', 'moskva')
        for bank_key, bank_value in bank_2.get_rate().items():
            self.assertTrue(isinstance(bank_value.rate_sell, float))

    def test_get_rate_bank_name_type_3(self):
        bank_3 = BankiRu('gbp', 'moskva')
        for bank_key, bank_value in bank_3.get_rate().items():
            self.assertTrue(isinstance(bank_key, str))

    def test_get_rate_curr_name_type_3(self):
        bank_3 = BankiRu('gbp', 'moskva')
        for bank_key, bank_value in bank_3.get_rate().items():
            self.assertTrue(isinstance(bank_value.name_currency, str))

    def test_get_rate_rate_buy_type_3(self):
        bank_3 = BankiRu('gbp', 'moskva')
        for bank_key, bank_value in bank_3.get_rate().items():
            self.assertTrue(isinstance(bank_value.rate_buy, float))

    def test_get_rate_rate_sell_type_3(self):
        bank_3 = BankiRu('gbp', 'moskva')
        for bank_key, bank_value in bank_3.get_rate().items():
            self.assertTrue(isinstance(bank_value.rate_sell, float))

    def test_get_rate_bank_name_type_4(self):
        bank_4 = BankiRu('jpy', 'moskva')
        for bank_key, bank_value in bank_4.get_rate().items():
            self.assertTrue(isinstance(bank_key, str))

    def test_get_rate_curr_name_type_4(self):
        bank_4 = BankiRu('jpy', 'moskva')
        for bank_key, bank_value in bank_4.get_rate().items():
            self.assertTrue(isinstance(bank_value.name_currency, str))

    def test_get_rate_rate_buy_type_4(self):
        bank_4 = BankiRu('jpy', 'moskva')
        for bank_key, bank_value in bank_4.get_rate().items():
            self.assertTrue(isinstance(bank_value.rate_buy, float))

    def test_get_rate_rate_sell_type_4(self):
        bank_4 = BankiRu('jpy', 'moskva')
        for bank_key, bank_value in bank_4.get_rate().items():
            self.assertTrue(isinstance(bank_value.rate_sell, float))
