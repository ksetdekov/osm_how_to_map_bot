import datetime
import sqlite3

from bs4 import BeautifulSoup
import bs4
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
    matches[i.text] = (Partial_Ratio, i)

x = sorted(matches, key=lambda k: matches[k][0], reverse=True)
print(matches[x[0]][0], x[0])  # находим раздел

# todo найти способ выбрать все между h3
# todo найти способ вывести это
# todo найти способ вывести это по запросу
position = h3s.index(matches[x[0]][1])

for header in h3s[position:position+1]:
    nextNode = header
    while True:
        nextNode = nextNode.nextSibling
        if nextNode is None:
            break
        if isinstance(nextNode, bs4.NavigableString):
            print(nextNode.strip())
        if isinstance(nextNode, bs4.Tag):
            if nextNode.name == "h3":
                break
            print(nextNode.get_text().strip())

now = datetime.datetime.now()
with open("parse.html", "w", newline='', encoding="utf-8") as f:
    f.write(how_to_map)

# read it back in
with open("parse.html", newline='', encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'lxml')
    # do something with soup
# set the limit how often to update
wait_time_to_update = datetime.timedelta(minutes=1)

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


def get_last_update():
    conn.execute("SELECT stamp FROM updates WHERE ok = 1 ORDER BY stamp DESC LIMIT 1")
    return datetime.datetime.strptime(conn.fetchone()[0], '%Y-%m-%d %H:%M:%S.%f')


print((datetime.datetime.now() - get_last_update()) > wait_time_to_update)


def get_soup(wait=1):
    now_time = datetime.datetime.now()
    wait_time = datetime.timedelta(minutes=wait)
    print()
    if (now_time - get_last_update()) > wait_time:
        print('get new')
    else:
        print('read from disk')


get_soup()
