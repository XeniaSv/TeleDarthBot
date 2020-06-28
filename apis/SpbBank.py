import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Rate = namedtuple('Rate', 'bank_name,name,rate_buy,rate_sell')


# Замена запятой на точку, так как в html записана запятая, а это не валидные данные
def str_to_float(item: str):
    item = item.replace(',', '.')
    return float(item)


# Парсер HTML страницы
def parser_HTML():
    url = 'https://www.bspb.ru/cash-rates'
    source = requests.get(url)
    main_text = source.text
    soup = BeautifulSoup(main_text)

    table = soup.find('table', {'class': 'table table-condensed'})
    return table.text.split('\n\n')


class SpbBank:
    info = None

    def __init__(self):
        self.info = parser_HTML()

    # Получение из HTML курс валюты USD
    def get_rates_USD(self):
        usd_info = self.info[11]
        usd_name = 'USD'
        usd_rate_buy = str_to_float(usd_info.split('\n')[2])
        usd_rate_sell = str_to_float(usd_info.split('\n')[3])
        return Rate(bank_name='Банк СПБ', name=usd_name, rate_buy=usd_rate_buy, rate_sell=usd_rate_sell)

    # Получение из HTML курс валюты EUR
    def get_rate_EUR(self):
        eur_info = self.info[7]
        eur_name = 'EUR'
        eur_rate_buy = str_to_float(eur_info.split('\n')[2])
        eur_rate_sell = str_to_float(eur_info.split('\n')[3])
        return Rate(bank_name='Банк СПБ', name=eur_name, rate_buy=eur_rate_buy, rate_sell=eur_rate_sell)
