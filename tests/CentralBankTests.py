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

    def test_get_rates_usd(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        usd = bank_1.get_rates_usd()
        self.assertEqual('USD', usd.name)
        self.assertEqual(30.9436, usd.rate)

        bank_2 = CentralBank(datetime.date(1900, 3, 20))
        with self.assertRaises(CbError):
            bank_2.get_rates_usd()

    def test_get_rates_eur(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        eur = bank_1.get_rates_eur()
        self.assertEqual('EUR', eur.name)
        self.assertEqual(26.8343, eur.rate)

        bank_4 = CentralBank(datetime.date(1900, 3, 20))
        with self.assertRaises(CbError):
            bank_4.get_rates_eur()

    def test_get_rates_gbp(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        gbp = bank_1.get_rates_gbp()
        self.assertEqual('GBP', gbp.name)
        self.assertEqual(43.8254, gbp.rate)

        bank_4 = CentralBank(datetime.date(1900, 3, 20))
        with self.assertRaises(CbError):
            bank_4.get_rates_gbp()

    def test_get_rates_jpy(self):
        bank_1 = CentralBank(datetime.date(2002, 3, 2))
        jpy = bank_1.get_rates_jpy()
        self.assertEqual('JPY', jpy.name)
        self.assertEqual(23.1527, jpy.rate)

        bank_4 = CentralBank(datetime.date(1900, 3, 20))
        with self.assertRaises(CbError):
            bank_4.get_rates_jpy()
