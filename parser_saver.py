import datetime
import sqlite3

from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz

# from lxml.html.clean import unicode

how_to_map = requests.get('https://wiki.openstreetmap.org/wiki/RU:%D0%9A%D0%B0%D0%BA_%D0%BE%D0%B1%D0%BE%D0%B7%D0%BD'
                          '%D0%B0%D1%87%D0%B8%D1%82%D1%8C').text
soup = BeautifulSoup(how_to_map, 'lxml')

h3s = soup.find_all('h3')
# тут вводится какое поиск мы делаем
Str2 = "здание"
matches = {}
for i in h3s:
    Str1 = i.text
    Partial_Ratio = fuzz.ratio(Str1.lower(), Str2.lower())
    print(i.text, Partial_Ratio)
    matches[i.text] = Partial_Ratio

x = sorted(matches, key=matches.get, reverse=True)
for k in x[:1]:
    print(matches[k], k)
    if matches[k] < 10:
        break

# todo найти способ выбрать все между h3
# todo найти способ вывести это
# todo найти способ вывести это по запросу


print(soup.find('h3').next_sibling)
now = datetime.datetime.now()
with open("parse.html", "w", newline='', encoding="utf-8") as f:
    f.write(how_to_map)

# read it back in
with open("parse.html", newline='', encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'lxml')
    # do something with soup
# set the limit how often to update
wait_time_to_update = datetime.timedelta(minutes=1)

print((datetime.datetime.now() - now) * 1000 > wait_time_to_update)

db = sqlite3.connect("data.sqlite")
conn = db.cursor()

conn.execute("""
CREATE TABLE IF NOT EXISTS "updates" (
    "stamp"	TEXT,
    "ok"	NUMERIC
);
""")


def add_time(status):
    conn.execute("INSERT INTO updates (stamp,ok) VALUES (?,?)", (datetime.datetime.now(), status))
    db.commit()


# add_time(1)


def get_last_update():
    conn.execute("SELECT stamp FROM updates WHERE ok = 1 ORDER BY stamp DESC LIMIT 1")
    return datetime.datetime.strptime(conn.fetchone()[0], '%Y-%m-%d %H:%M:%S.%f')


print((datetime.datetime.now() - get_last_update()) > wait_time_to_update)
print((datetime.datetime.now() - get_last_update()))
print(wait_time_to_update)
