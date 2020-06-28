from collections import namedtuple
import xmltodict
import requests

Rate = namedtuple('Rate', 'bank_name,name,rate')


# Парсер xml
def parser_xml():
    # URL запроса
    url = "https://www.vtb-bank.by/sites/default/files/rates.xml"

    r = requests.get(url)
    resp = r.text

    return xmltodict.parse(resp)


class VtbBank:
    info = None

    def __init__(self):
        self.info = parser_xml()

    # Получение из JSON курс валюты USD
    def get_rates_USD(self):
        # Параметры поиска по JSON
        section_code_from = 'usd'
        section_code_to = 'rub'

        for item in self.info['rates']['conversion']['rate']:
            if (item['codeFrom'] == section_code_from) and (item['codeTo'] == section_code_to):
                r = Rate(
                    bank_name='ВТБ',
                    name=item['codeFrom'].upper(),
                    rate=item['value']
                )
                return r
        return None

    # Получение из JSON курс валюты EUR
    def get_rates_EUR(self):
        # Параметры поиска по JSON
        section_code_from = 'eur'
        section_code_to = 'rub'

        for item in self.info['rates']['conversion']['rate']:
            if (item['codeFrom'] == section_code_from) and (item['codeTo'] == section_code_to):
                r = Rate(
                    bank_name='ВТБ',
                    name=item['codeFrom'].upper(),
                    rate=item['value']
                )
                return r
        return None
