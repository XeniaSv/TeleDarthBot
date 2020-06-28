import datetime
from collections import namedtuple
import xmltodict
import requests

Rate = namedtuple('Rate', 'bank_name,name,rate')


# Замена запятой на точку, так как json возращает запятую
def str_to_float(item: str):
    item = item.replace(',', '.')
    return float(item)


# Парсер xml
def parser_xml():
    # URL запроса
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    # Формат даты: день/месяц/год
    date_format = "%d/%m/%Y"

    # Дата запроса
    today = datetime.datetime.today()
    params = {
        "date_req": today.strftime(date_format),
    }
    r = requests.get(url, params=params)
    resp = r.text

    return xmltodict.parse(resp)


class CbBank:
    info = None

    def __init__(self):
        self.info = parser_xml()

    # Получение из JSON курс валюты USD
    def get_rates_USD(self):
        # Параметры поиска по JSON
        section_id_USD = 'R01235'

        for item in self.info['ValCurs']['Valute']:
            if item['@ID'] == section_id_USD:
                r = Rate(
                    bank_name='Центробанк',
                    name=item['CharCode'],
                    rate=str_to_float(item['Value'])
                )
                return r
        return None

    # Получение из JSON курс валюты EUR
    def get_rates_EUR(self):
        # Параметры поиска по JSON
        section_id_EUR = 'R01239'

        for item in self.info['ValCurs']['Valute']:
            if item['@ID'] == section_id_EUR:
                r = Rate(
                    bank_name='Центробанк',
                    name=item['CharCode'],
                    rate=str_to_float(item['Value'])
                )
                return r
        return None
