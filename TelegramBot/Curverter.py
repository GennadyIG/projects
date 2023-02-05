import telebot
from extensions import *
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def hello(message):
    bot.send_message(message.chat.id, f'{message.chat.first_name}, приветствую в конвертере валют.\n'
                                      f'Для конвертации необходимо ввести аббревиатуры валют и сумму,\n'
                                      f'например для конвертации 100 евро в рубли необходимо ввести в чат:\n'
                                      f' "eur rub 100".\nВот некоторые валюты:\nRUB: Российский рубль\nEUR: Евро\n'
                                      f'JPY: Японская йена\nCNY: Китайский юань\nUSD: Американский доллар\n'
                                      f'TRY: Турецкая лира\n'
                                      f'Для просмотра всех доступных валют введите команду "/values"')


@bot.message_handler(commands=['values'])
def all_currency(message):
    bot.send_message(message.chat.id, f'{Converter.print_currency()}')


@bot.message_handler(content_types=['text'])
def function_convert(message):
    teleuser = InputHandling(message.text)
    convert = teleuser.message_to_list()
    bot.reply_to(message, f"{convert}")


bot.polling(none_stop=True)
