import unittest
import datetime
import random

from apis.centralBank import CentralBank
from apis.centralBank import CbError
from apis.centralBank import parser_cb_xml
from apis.centralBank import str_to_float


class CentralBankTests(unittest.TestCase):
    def test_parser_cb_xml_is_not_none(self):
        self.assertIsNotNone(parser_cb_xml(datetime.date(2002, 3, 2)))

    def test_str_to_float(self):
        number = random.random()
        self.assertEqual(number, str_to_float(f'{number}'))

    def test_get_rates_currency_name_usd(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        usd = bank_1.get_rates_usd()
        self.assertEqual('USD', usd.name)

    def test_get_rates_rate_usd(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        usd = bank_1.get_rates_usd()
        self.assertEqual(30.9436, usd.rate)

    def test_get_rates_usd_error(self):
        bank_2 = CentralBank(datetime.date(1900, 3, 20))
        with self.assertRaises(CbError):
            bank_2.get_rates_usd()

    def test_get_rates_currency_name_eur(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        eur = bank_1.get_rates_eur()
        self.assertEqual('EUR', eur.name)

    def test_get_rates_rate_eur(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        eur = bank_1.get_rates_eur()
        self.assertEqual(26.8343, eur.rate)

    def test_get_rates_eur_error(self):
        bank_4 = CentralBank(datetime.date(1900, 3, 20))
        with self.assertRaises(CbError):
            bank_4.get_rates_eur()

    def test_get_rates_currency_name_gbp(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        gbp = bank_1.get_rates_gbp()
        self.assertEqual('GBP', gbp.name)

    def test_get_rates_rate_gbp(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        gbp = bank_1.get_rates_gbp()
        self.assertEqual(43.8254, gbp.rate)

    def test_get_rates_gbp_error(self):
        bank_4 = CentralBank(datetime.date(1900, 3, 20))
        with self.assertRaises(CbError):
            bank_4.get_rates_gbp()

    def test_get_rates_currency_name_jpy(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        jpy = bank_1.get_rates_jpy()
        self.assertEqual('JPY', jpy.name)

    def test_get_rates_rate_jpy(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        jpy = bank_1.get_rates_jpy()
        self.assertEqual(23.1527, jpy.rate)

    def test_get_rates_jpy_error(self):
        bank_4 = CentralBank(datetime.date(1900, 3, 20))
        with self.assertRaises(CbError):
            bank_4.get_rates_jpy()
