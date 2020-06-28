import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Rate = namedtuple('Rate', 'bank_name,name,rate_buy,rate_sell')


# Парсер HTML страницы
def parser_HTML():
    url = 'https://www.raiffeisen.ru/currency_rates/'

    source = requests.get(url)
    main_text = source.text
    soup = BeautifulSoup(main_text)

    table = soup.find_all('div', {'class': 'b-table__row'})

    return table


class RaiffasenBank:
    info = None

    def __init__(self):
        self.info = parser_HTML()

    # Получение из HTML курс валюты USD
    def get_rates_USD(self):
        usd_info = self.info[0].text.split('\n')
        usd_name = usd_info[1]
        usd_rate_buy = usd_info[4]
        usd_rate_sell = usd_info[6].replace(' ', '')
        return Rate(bank_name='Райффайзенбанк', name=usd_name, rate_buy=usd_rate_buy, rate_sell=usd_rate_sell)

    # Получение из HTML курс валюты EUR
    def get_rates_EUR(self):
        eur_info = self.info[1].text.split('\n')
        eur_name = eur_info[1]
        eur_rate_buy = eur_info[4]
        eur_rate_sell = eur_info[6].replace(' ', '')
        return Rate(bank_name='Райффайзенбанк', name=eur_name, rate_buy=eur_rate_buy, rate_sell=eur_rate_sell)
