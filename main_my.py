import pandas as pd
import requests
import telebot
from bs4 import BeautifulSoup

import config_my

bot = telebot.TeleBot(config_my.token)





@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(message.chat.id, 'hello')


@bot.message_handler(commands=["help"])
def hello(message):
    bot.reply_to(message, "how are you doing")


@bot.message_handler(func=lambda message: message.text.lower().strip() != '/start')
def echo(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.infinity_polling()

# мы хотим finite state machine
