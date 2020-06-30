import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from logging import getLogger

Rate = namedtuple('Rate', 'name_currency,rate_buy,rate_sell')
logger = getLogger(__name__)


def str_to_float(item: str):
    item = item.replace(',', '.')
    return float(item)


class ParserError(Exception):
    """Неизвестная ошибка при запросе Api BankiRu"""


# Парсер HTML страницы BankiRu
def parser_HTML(currency_name: str, country_name: str):
    url = 'https://www.banki.ru/products/currency/cash'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    curr_url = url + f'/{currency_name}/{country_name}/'

    try:
        source = requests.get(curr_url, headers=headers)
        main_text = source.text
        soup = BeautifulSoup(main_text, 'html.parser')

        convert = soup.find_all('div', {'class': 'exchange-calculator-rates table-flex__row-group'})

        return convert
    except Exception:
        logger.exception("Parser error")
        raise ParserError


def get_rate(currency_name: str, country_name: str):
    banks = dict()
    try:
        for info in parser_HTML(currency_name, country_name):
            info_bank = info.find('div', {'class': 'table-flex__row item calculator-hover-icon__container'})
            bank_name = info_bank.find('a', {'data-test': 'bank-name'})

            rate_info = info_bank.find_all('div', {'data-currencies-code': currency_name.upper()})

            rate_buy = str_to_float(rate_info[0].text.split('\n\n')[0].lstrip().strip().replace(' ₽', ''))

            rate_sell = str_to_float(rate_info[1].text.split('\n\n')[0].lstrip().strip().replace(' ₽', ''))

            banks[bank_name.text] = Rate(name_currency=currency_name.upper(), rate_buy=float(rate_buy),
                                         rate_sell=float(rate_sell))
        return banks

    except Exception:
        logger.exception("Get rate error")
        raise AttributeError


if __name__ == '__main__':
    try:
        banks_main = get_rate('usd', 'moskva')
        for key, value in banks_main.items():
            print(key, value)
    except ParserError:
        logger.info('Parser error')
    except AttributeError:
        logger.info('Attribute error')