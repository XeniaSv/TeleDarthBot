import datetime
import http
import xmltodict
import requests
from collections import namedtuple

# Небольшая обертка, которая имеет поля название курса, курс валюты
Rate = namedtuple('Rate', 'name,rate')


class CbError(Exception):
    """Ошибка при запросе API сайта CB"""


def parser_cb_xml(date: datetime.date):
    """
    Функция парсинга xml страницы Центробанка
    :param date: дата, по которой нужно узнать курс
    :return: информацию о курсах валют на текущее число в формате JSON
    """
    get_curl = 'http://www.cbr.ru/scripts/XML_daily.asp'
    date_format = "%d/%m/%Y"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    params = {
        "date_req": date.strftime(date_format)
    }

    source = requests.get(get_curl, params=params, headers=headers)
    if source.status_code != http.HTTPStatus.OK:
        raise CbError('Плохой статус код')

    try:
        info = source.text
        return xmltodict.parse(info)
    except xmltodict.expat.error:
        raise CbError('Плохой файл xml')


def str_to_float(item: str):
    """
    Функция заменяющая запятую на точку
    :param item: строка
    :return: число типа float
    """
    item = item.replace(',', '.')
    return float(item)


class CentralBank:
    """
    Класс CbBank
    """
    __info = None

    def __init__(self, date: datetime.date):
        """
        Конструктор
        :param date: дата, по которой надо узнать курс
        """
        self.__info = parser_cb_xml(date)

    def get_rates_usd(self):
        """
        Найти курс usd
        :return: ифнормация в namedtuple Rate
        """
        section_id = 'R01235'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    rate = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return rate
            return None

        except (KeyError, TypeError, ValueError):
            raise CbError('Ошибка поиска информации по JSON')

    def get_rates_eur(self):
        """
        Найти курс eur
        :return: ифнормация в namedtuple Rate
        """
        section_id = 'R01239'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    rate = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return rate
            return None

        except (KeyError, TypeError, ValueError):
            raise CbError('Ошибка поиска информации по JSON')

    def get_rates_gbp(self):
        """
        Найти курс gbp
        :return: ифнормация в namedtuple Rate
        """
        section_id = 'R01035'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    rate = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return rate
            return None
        except (KeyError, TypeError, ValueError):
            raise CbError('Ошибка поиска информации по JSON')

    def get_rates_jpy(self):
        """
        Найти курс jpy
        :return: ифнормация в namedtuple Rate
        """
        section_id = 'R01820'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    rate = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return rate
            return None
        except (KeyError, TypeError, ValueError):
            raise CbError('Ошибка поиска информации по JSON')


if __name__ == '__main__':
    try:
        bank = CentralBank(datetime.date(2020, 7, 3))
        print(bank.get_rates_usd())
        print(bank.get_rates_eur())
        print(bank.get_rates_gbp())
        print(bank.get_rates_jpy())
    except CbError:
        print('Error')
