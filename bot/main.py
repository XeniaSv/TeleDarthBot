from datetime import datetime

from apis.cbRF import CbBank
from apis.VTBBank import VtbBank
from apis.BankNeva import BankNeva
from apis.Raiffasen import RaiffasenBank
from apis.SpbBank import SpbBank
from apis.EastBank import EastBank
from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from bot.config import TOKEN


# Функция старт бота
def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Напиши мне что-нибудь",
    )


# Функция help бота
def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Это бот\n\n"
             "Список доступных команд есть в меню\n\n"
             "Также я отвечу на любое сообщение",
    )


# Функция time(Время на сервере) бота
def do_time(bot: Bot, update: Update):
    now = datetime.now()
    text = "{}.{}.{} {}:{}:{}".format(now.day, now.month, now.year, now.hour, now.minute, now.second)
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Дата и время на сервере: \n{}".format(text),
    )


# Список валют
def do_currency(bot: Bot, update: Update):
    cb_bank = CbBank()
    item_from_CB_usd = cb_bank.get_rates_USD()
    item_from_CB_eur = cb_bank.get_rates_EUR()
    message_from_CB_bank = f'{item_from_CB_usd.bank_name}\n' \
                           + f'Курс {item_from_CB_usd.name} = {item_from_CB_usd.rate} руб' \
                           + '\n' \
                           + f'Курс {item_from_CB_eur.name} = {item_from_CB_eur.rate} руб\n\n'

    vtb_bank = VtbBank()
    item_from_VTB_usd = vtb_bank.get_rates_USD()
    item_from_VTB_eur = vtb_bank.get_rates_EUR()
    message_from_VTB_bank = f'{item_from_VTB_usd.bank_name}:\n' \
                            + f'Курс {item_from_VTB_usd.name} = {item_from_VTB_usd.rate} руб' \
                            + '\n' \
                            + f'Курс {item_from_VTB_eur.name} = {item_from_VTB_eur.rate} руб\n\n'

    bank_neva = BankNeva()
    item_from_Bank_Neva_usd = bank_neva.get_rates_USD()
    item_from_Bank_Neva_eur = bank_neva.get_rates_EUR()
    message_from_Bank_Neva = f'{item_from_Bank_Neva_usd.bank_name}:\n' \
                             + f'Покупка: {item_from_Bank_Neva_usd.name} = {item_from_Bank_Neva_usd.rate_buy} руб' \
                             + '\n' \
                             + f'Продажа: {item_from_Bank_Neva_usd.name} = {item_from_Bank_Neva_usd.rate_sell} руб\n' \
                             + f'Покупка: {item_from_Bank_Neva_eur.name} = {item_from_Bank_Neva_eur.rate_buy} руб' \
                             + '\n' \
                             + f'Продажа: {item_from_Bank_Neva_eur.name} = {item_from_Bank_Neva_eur.rate_sell} руб\n\n'

    raiffasen_bank = RaiffasenBank()
    item_from_Raiffasen_bank_usd = raiffasen_bank.get_rates_USD()
    item_from_Raiffasen_bank_eur = raiffasen_bank.get_rates_EUR()
    message_from_Raiffasen_bank = f'{item_from_Raiffasen_bank_usd.bank_name}:\n' \
                                  + f'Покупка: {item_from_Raiffasen_bank_usd.name} = {item_from_Raiffasen_bank_usd.rate_buy} руб' \
                                  + '\n' \
                                  + f'Продажа: {item_from_Raiffasen_bank_usd.name} = {item_from_Raiffasen_bank_usd.rate_sell} руб\n' \
                                  + f'Покупка: {item_from_Raiffasen_bank_eur.name} = {item_from_Raiffasen_bank_eur.rate_buy} руб' \
                                  + '\n' \
                                  + f'Продажа: {item_from_Raiffasen_bank_eur.name} = {item_from_Raiffasen_bank_eur.rate_sell} руб\n\n'

    spb_bank = SpbBank()
    item_from_Spb_bank_usd = spb_bank.get_rates_USD()
    item_from_Spb_bank_eur = spb_bank.get_rate_EUR()
    message_from_Spb_bank = f'{item_from_Spb_bank_usd.bank_name}:\n' \
                             + f'Покупка: {item_from_Spb_bank_usd.name} = {item_from_Spb_bank_usd.rate_buy} руб' \
                             + '\n' \
                             + f'Продажа: {item_from_Spb_bank_usd.name} = {item_from_Spb_bank_usd.rate_sell} руб\n' \
                             + f'Покупка: {item_from_Spb_bank_eur.name} = {item_from_Spb_bank_eur.rate_buy} руб' \
                             + '\n' \
                             + f'Продажа: {item_from_Spb_bank_eur.name} = {item_from_Spb_bank_eur.rate_sell} руб\n\n'

    east_bank = EastBank()
    item_from_East_bank_usd = east_bank.get_rates_USD()
    item_from_East_bank_eur = east_bank.get_rates_EUR()
    message_from_East_bank = f'{item_from_East_bank_usd.bank_name}:\n' \
                             + f'Покупка: {item_from_East_bank_usd.name} = {item_from_East_bank_usd.rate_buy} руб' \
                             + '\n' \
                             + f'Продажа: {item_from_East_bank_usd.name} = {item_from_East_bank_usd.rate_sell} руб\n' \
                             + f'Покупка: {item_from_East_bank_eur.name} = {item_from_East_bank_eur.rate_buy} руб' \
                             + '\n' \
                             + f'Продажа: {item_from_East_bank_eur.name} = {item_from_East_bank_eur.rate_sell} руб\n\n'

    bot.send_message(
        chat_id=update.message.chat_id,
        text=message_from_CB_bank +
             message_from_VTB_bank +
             message_from_Bank_Neva +
             message_from_Raiffasen_bank +
             message_from_Spb_bank +
             message_from_East_bank,
    )


# Функция echo(повтор сообщений) бота
def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = "Твой ID = {}\n\n{}".format(chat_id, update.message.text)

    bot.send_message(
        chat_id=chat_id,
        text=text,
    )


# Main
def main():
    bot = Bot(
        token=TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    time_handler = CommandHandler("time", do_time)
    currency_handler = CommandHandler("currency", do_currency)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(currency_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
