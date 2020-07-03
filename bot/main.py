import telebot
from datetime import datetime
import re

from bot.config import TOKEN

from info.DAO import currencies
from info.DAO import cities

from apis.centralBank import CentralBank
from apis.centralBank import CbError

from apis.BankiRu import BankiRu
from apis.BankiRu import BankiRuError

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def do_start(message):
    """
    Функция старта
    :param message: сообщение пользователя
    :return: сообщение о старте
    """
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Привет! Давай узнаем курс валют. Чтобы узнать подробности напиши /help'
    )


@bot.message_handler(commands=['help'])
def do_help(message):
    """
    Функция помощи
    :param message: сообщение пользователя
    :return: сообщение о помощи
    """
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Я Darth Bot. Почти как Darth Vader, только я повстанец.\n\n'
             'Я могу узнать курс валют в городах с помощью сайта Banki.ru.'
             'Чтобы сделать это тебе нужно ввести предложение, в котором содержится название валюты на русском'
             '(доллар, евро, фунт, иена, юань) и город, в котором ты хочешь узнать информацию.\n\n'
             'Чтобы узнать какие города поддерживаются напиши /cities\n\n'
             'Чтобы узнать курс валюты из ЦБ напиши /centralbank *Валюты на русском языке* *Дата в формате ДЕНЬ-МЕСЯЦ-ГОД*\n\n'
             'Да прибудет с тобой сила!'
    )


@bot.message_handler(commands=['cities'])
def do_cities(message):
    """
    Функция вывода всех городов
    :param message: сообщение от пользователя
    :return: список городов
    """
    chat_id = message.chat.id
    text = 'Вот тебе города. Скоро мы будем во всей галактике\n\n'
    for city in cities.keys():
        text += f'{city}\n'
    bot.send_message(
        chat_id=chat_id,
        text=text
    )


@bot.message_handler(commands=['centralbank'])
def do_central_bank(message):
    """
    Функция поиска курса заданной валюты и даты в Центробанке
    :param message: сообщение пользователя
    :return: курс валюты на заданное число
    """
    chat_id = message.chat.id
    try:
        text = str(message.text).lower()
        result = re.findall(r'доллар|евр|фунт|иен|', text)
        result += re.findall(r'\d*-\d*-\d*', text)
        result = list(filter(lambda a: a != '', result))

        if len(result) == 2:
            date_format = "%d-%m-%Y"
            date = datetime.strptime(result[1], date_format)

            text = f'Вот данные из центробанка\n{date.strftime(date_format)}\n'
            bank = CentralBank(date)

            if result[0] == 'доллар':
                rate = bank.get_rates_usd()
                text += f'{rate.name} = {rate.rate} руб.'
                bot.send_message(
                    chat_id=chat_id,
                    text=text
                )

            if result[0] == 'eвр':
                rate = bank.get_rates_eur()
                text += f'{rate.name} = {rate.rate} руб.'
                bot.send_message(
                    chat_id=chat_id,
                    text=text
                )

            if result[0] == 'фунт':
                rate = bank.get_rates_gbp()
                text += f'{rate.name} = {rate.rate} руб.'
                bot.send_message(
                    chat_id=chat_id,
                    text=text
                )

            if result[0] == 'иен':
                rate = bank.get_rates_jpy()
                text += f'{rate.name} = {rate.rate} руб.'
                bot.send_message(
                    chat_id=chat_id,
                    text=text
                )
        else:
            text = 'Прости, но ты ввел команду не правильно. Тебя никогда не примут в орден джедаев!'
            bot.send_message(
                chat_id=chat_id,
                text=text
            )
    except CbError:
        text = 'Данная дата выходит за пределы. "В пределы поспасть должен ты" © Йода'
        bot.send_message(
            chat_id=chat_id,
            text=text
        )
    except ValueError:
        text = 'Ваша дата невалидна. "Головой думать должен ты" © Йода'
        bot.send_message(
            chat_id=chat_id,
            text=text
        )


@bot.message_handler(content_types=['text'])
def do_text(message):
    """
    Функция ответа на сообщение
    :param message: сообщение от пользователя
    :return: сообщение пользователю
    """
    if message.chat.type == "private":
        chat_id = message.chat.id
        text = str(message.text).lower()
        text = get_text_from_bankiRu(text)

        bot.send_message(
            chat_id=chat_id,
            text=text
        )

    if message.chat.type == "group":
        chat_id = message.chat.id
        text = str(message.text).lower()
        if text.find('@Currency_Darth_bot'.lower()) > -1:
            text = get_text_from_bankiRu(text)

            bot.send_message(
                chat_id=chat_id,
                text=text
            )


def get_text_from_bankiRu(text):
    """
    Функция поиска курса валюты в городе
    :param text: исходный текст пользователя
    :return: строка с информацией
    """
    result = re.findall(r'доллар|евр|фунт|иен|юан', text)
    result += re.findall(
        r'благовещенск|архангельск|астрахан|белгород|брянск|владимир|волгоград|вологд|воронеж|иванов|иркутск|'
        r'калининград|калуг|петропавловс|кемерово|киров|костром|курган|курск|санкт-петербург|липецк|магадан|'
        r'москв|мурманск|нижн|велик|новосибирск|омск|оренбург|пенз|перм|псков|ростов|рязан|самар|саратов|'
        r'южн|екатеринбург|смоленск|тамбов|тул|тюмен|ульяновск|челябинск|чит|ярославл|майкоп|горно-алтайск|'
        r'уф|улан-уде|махачкал|биробиджан|нальчик|элист|черкесск|петрозавосдск|сыктывкар|симферопол|йошкар-ол|'
        r'саранск|якутск|владикавказ|казан|кызыл|ижевск|абакан|грозн|чебоксар|барнаул|краснодар|красноярск|'
        r'владивосток|ставропол|хабаровск|нарьян-мар|ханты-мансийск|анадыр|салехард', text
    )
    result = list(filter(lambda a: a != '', result))

    if len(result) == 2:
        text = ''
        city_url = ''
        for city_key, city_value in cities.items():
            if city_key.lower().find(result[1].lower()) > -1:
                city_url = city_value
                text += f'город {city_key}\n'
                break

        currency_url = ''
        for currency_key, currency_value in currencies.items():
            if currency_key.lower().find(result[0].lower()) > -1:
                currency_url = currency_value
                text += f'{currency_key}\n\n'
                break

        try:
            bankiRu = BankiRu(currency_url, city_url)
            banks = bankiRu.get_rate()

            if len(banks) >= 5:
                i = 0
                for bank_key, bank_value in banks.items():
                    if i < 5:
                        text += f'{bank_key}\nПокупка: {bank_value.rate_buy} руб\nПродажа: {bank_value.rate_sell} руб\n\n'
                        i += 1

            elif len(banks) == 0:
                text += 'К сожалению этой валюты нет в городе. Её украл Хан Соло'

            else:
                for bank_key, bank_value in banks.items():
                    text += f'{bank_key}\nПокупка: {bank_value.rate_buy} руб\nПродажа: {bank_value.rate_sell} руб\n\n'

            return text

        except BankiRuError:
            text = 'Произошла ошибка. Its a trap!'
            return text
    else:
        text = 'Я ничего не нашел по твоему запросу. Только ситхи всё возводят в абсолют!'
        return text


@bot.message_handler(content_types=["sticker"])
def answer_sticker(message):
    if message.chat.type == "private":
        bot.send_message(
            chat_id=message.chat.id,
            text="\U0001F31A"
        )


@bot.message_handler(content_types=["photo"])
def answer_photo(message):
    """
    Функция ответа на стикер
    :param message: сообщение от пользователя
    :return: moon face
    """
    if message.chat.type == "private":
        bot.send_message(
            chat_id=message.chat.id,
            text="\U0001F31A"
        )


@bot.message_handler(content_types=["audio"])
def answer_audio(message):
    """
    Функция ответа на аудио
    :param message: сообщение от пользователя
    :return: moon face
    """
    if message.chat.type == "private":
        bot.send_message(
            chat_id=message.chat.id,
            text="\U0001F31A"
        )


@bot.message_handler(content_types=["document"])
def answer_document(message):
    """
    Функция ответа на документ
    :param message: сообщение от пользователя
    :return: moon face
    """
    if message.chat.type == "private":
        bot.send_message(
            chat_id=message.chat.id,
            text="\U0001F31A"
        )


bot.polling(none_stop=True, interval=0)
