import config_my
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from tabulate import tabulate
import telebot
print(config_my.token)
bot = telebot.TeleBot(config_my.token)

pict = [
    'https://avatars.mds.yandex.net/get-pdb/2864819/2091b635-1a05-4a81-9f4f-9cdd46cb9be0/s1200',
    'https://avatars.mds.yandex.net/get-zen_doc/196516/pub_5d65e93efe289100adb4c54e_5d66099378125e00ac052d00/scale_1200',
    'https://avatars.mds.yandex.net/get-pdb/1683100/d71b5f09-b408-42ce-b480-cbcd0d340efe/s1200?webp=false',
    'https://avatars.mds.yandex.net/get-zen_doc/1899089/pub_5d9b5f2f35c8d800ae71fb5a_5d9b60a98f011100b48eb4fb/scale_1200',
    'https://avatars.mds.yandex.net/get-zen_doc/196516/pub_5d65e93efe289100adb4c54e_5d66099378125e00ac052d00/scale_1200',
    'http://ysia.ru/wp-content/uploads/2018/01/1-19.jpg'
    ]

def stat(tag=0):
    url = 'https://www.worldometers.info/coronavirus/'
    website = requests.get(url).text
    soup = BeautifulSoup(website, 'lxml')
    table = soup.find_all('table')[tag]
    rows = table.find_all('tr')
    fields_list = []

    for i in range(9):
        col = list()
        col.append(rows[0].find_all('th')[i + 1].get_text().strip())
        for row in rows[1:224]:
            r = row.find_all('td')
            col.append(r[i + 1].get_text().strip())
        fields_list.append(col)
    d = dict()
    for i in range(9):
        d[fields_list[i][0]] = fields_list[i][1:]
    df = pd.DataFrame(d)
    df = df.rename(columns={'Country,Other': 'Country', 'Serious,Critical': 'SeriousCritical'})
    return df


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
