import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Rate = namedtuple('Rate', 'bank_name,name,rate_buy,rate_sell')


# Парсер HTML страницы
def parser_HTML(flag):
    # Для USD
    if flag:
        url = 'https://vostobank.ru/exchange.html'

        source = requests.get(url)
        main_text = source.text
        soup = BeautifulSoup(main_text)

        table = soup.find('table', {'class': 'table ser ser1'}).text

        curr_table = [i for i in table.split('\n') if i]

        return curr_table

    # Для EUR
    else:
        url = 'https://vostobank.ru/exchange.html'

        source = requests.get(url)
        main_text = source.text
        soup = BeautifulSoup(main_text)

        table = soup.find('table', {'class': 'table ser ser2'}).text

        curr_table = [i for i in table.split('\n') if i]

        return curr_table


class EastBank:
    info_usd = None
    info_eur = None

    def __init__(self):
        self.info_usd = parser_HTML(True)
        self.info_eur = parser_HTML(False)

    # Получение из HTML курс валюты USD
    def get_rates_USD(self):
        usd_rate_buy = self.info_usd[6]
        usd_rate_sell = self.info_usd[5]
        return Rate(bank_name='Восточный банк', name='USD', rate_buy=usd_rate_buy, rate_sell=usd_rate_sell)

    # Получение из HTML курс валюты EUR
    def get_rates_EUR(self):
        eur_rate_buy = self.info_eur[6]
        eur_rate_sell = self.info_eur[5]
        return Rate(bank_name='Восточный банк', name='EUR', rate_buy=eur_rate_buy, rate_sell=eur_rate_sell)
