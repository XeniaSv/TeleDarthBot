import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Rate = namedtuple('Rate', 'bank_name,name,rate_buy,rate_sell')


# Замены запятой на точку, так как в html записана запятая, а это не валидные данные
def str_to_float(item: str):
    item = item.replace(',', '.')
    return float(item)


# Парсер HTML страницы
def parser_HTML():
    url = 'https://neyvabank.ru/kursy-valyut'

    source = requests.get(url)
    main_text = source.text
    soup = BeautifulSoup(main_text)

    table = soup.find('table', {'class': 'currency-table'})

    return table.text.split('\n\n\n')


class BankNeva:
    info = None

    def __init__(self):
        self.info = parser_HTML()

    # Получение из HTML курс валюты USD
    def get_rates_USD(self):
        usd_name = self.info[1].split('\n')[0]
        usd_rate_buy = str_to_float(self.info[1].split('\n')[1])
        usd_rate_sell = str_to_float(self.info[1].split('\n')[2])

        return Rate(bank_name='Банк Нева', name=usd_name, rate_buy=usd_rate_buy, rate_sell=usd_rate_sell)

    # Получение из HTML курс валюты EUR
    def get_rates_EUR(self):
        eur_name = self.info[2].split('\n')[0]
        eur_rate_buy = str_to_float(self.info[2].split('\n')[1])
        eur_rate_sell = str_to_float(self.info[2].split('\n')[2])

        return Rate(bank_name='Банк Нева', name=eur_name, rate_buy=eur_rate_buy, rate_sell=eur_rate_sell)
