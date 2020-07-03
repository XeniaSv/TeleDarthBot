import http
import requests
from bs4 import BeautifulSoup
from collections import namedtuple

# Небольшая обертка, которая имеет поля название курса, курс покупки, курс продажи
Rate = namedtuple('Rate', 'name_currency,rate_buy,rate_sell')


class BankiRuError(Exception):
    """Неизвестная ошибка при запросе Api BankiRu"""


def str_to_float(item: str):
    """
    Функция заменяющая запятую на точку
    :param item: строка
    :return: число типа float
    """
    item = item.replace(',', '.')
    return float(item)


def parser_HTML(currency_name: str, city_name: str):
    """
    Функция парсинга html страницы BankiRu
    :param currency_name: название валюты
    :param city_name: название города
    :return: информацию о банках с сайта BankiRu
    """
    url = 'https://www.banki.ru/products/currency/cash'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    curr_url = url + f'/{currency_name}/{city_name}/'
    source = requests.get(curr_url, headers=headers)
    if source.status_code != http.HTTPStatus.OK:
        raise BankiRuError('Bad status code')

    main_text = source.text
    soup = BeautifulSoup(main_text, 'html.parser')

    convert = soup.find_all('div', {'class': 'exchange-calculator-rates table-flex__row-group'})

    return convert


class BankiRu:
    """
    Класс BankiRu
    """
    __info = None
    __currency_name = None
    __city_name = None

    def __init__(self, currency_name: str, city_name: str):
        """
        Конструктор
        :param currency_name: название валюты
        :param city_name: название города
        """
        self.__currency_name = currency_name
        self.__city_name = city_name
        self.__info = parser_HTML(self.__currency_name, self.__city_name)

    def get_rate(self):
        """
        Функция вычелениющая ифнормацию о курсе валют из каждого банка
        :return: словарь, ключем которого является название банка, значением является ифнормация о курсе в namedtuple Rate
        """
        banks = dict()
        try:
            for info in self.__info:
                info_bank = info.find('div', {'class': 'table-flex__row item calculator-hover-icon__container'})
                bank_name = info_bank.find('a', {'data-test': 'bank-name'})

                rate_info = info_bank.find_all('div', {'data-currencies-code': self.__currency_name.upper()})

                rate_buy = str_to_float(rate_info[0].text.split('\n\n')[0].lstrip().strip().replace(' ₽', ''))

                rate_sell = str_to_float(rate_info[1].text.split('\n\n')[0].lstrip().strip().replace(' ₽', ''))

                banks[bank_name.text] = Rate(name_currency=self.__currency_name.upper(), rate_buy=rate_buy,
                                             rate_sell=rate_sell)
            return banks

        except AttributeError:
            raise BankiRuError


if __name__ == '__main__':
    try:
        banks_info = BankiRu('gbp', 'kazan~')
        for key, value in banks_info.get_rate().items():
            print(key, value)
    except BankiRuError:
        print('Ошибка')
