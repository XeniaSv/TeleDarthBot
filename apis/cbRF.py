from logging import getLogger
import datetime

import xmltodict
import requests
from collections import namedtuple

logger = getLogger(__name__)
Rate = namedtuple('Rate', 'name,rate')


class ParserError(Exception):
    """Неизвестная ошибка при запросе API CB"""


def parser_cb_xml(date_now: datetime.date):
    get_curl = 'http://www.cbr.ru/scripts/XML_daily.asp'
    date_format = "%d/%m/%Y"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    params = {
        "date_req": date_now.strftime(date_format)
    }

    try:
        r = requests.get(get_curl, params=params, headers=headers)
        resp = r.text
        return xmltodict.parse(resp)
    except Exception:
        logger.exception("Parser error")
        raise ParserError


def str_to_float(item: str):
    item = item.replace(',', '.')
    return float(item)


class CbBank:
    __info = None

    def __init__(self, date_now: datetime.date):
        self.__info = parser_cb_xml(date_now)

    def get_rates_usd(self):
        section_id = 'R01235'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    r = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return r
            return None

        except Exception:
            logger.exception("Invalid key")
            raise KeyError

    def get_rates_eur(self):
        section_id = 'R01239'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    r = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return r
            return None

        except Exception:
            logger.exception("Invalid key")
            raise KeyError

    def get_rates_gbp(self):
        section_id = 'R01035'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    r = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return r
            return None
        except Exception:
            logger.exception("Invalid key")
            raise KeyError

    def get_rates_jpy(self):
        section_id = 'R01820'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    r = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return r
            return None
        except Exception:
            logger.exception("Invalid key")
            raise KeyError


if __name__ == '__main__':
    try:
        bank = CbBank(datetime.date(2018, 8, 2))
        print(bank.get_rates_usd())
        print(bank.get_rates_eur())
        print(bank.get_rates_gbp())
        print(bank.get_rates_jpy())
    except KeyError:
        logger.info("Invalid key")
    except ParserError:
        logger.info("Parser error")
    except ValueError:
        logger.info("Value error")
