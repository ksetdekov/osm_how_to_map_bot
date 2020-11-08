import datetime
import sqlite3

from bs4 import BeautifulSoup
import bs4
import requests
from fuzzywuzzy import fuzz

# set db connection
db = sqlite3.connect("data.sqlite")
conn = db.cursor()

conn.execute("""
CREATE TABLE IF NOT EXISTS "updates" (
    "stamp"	TEXT,
    "ok"	NUMERIC
);
""")


def add_time(status):
    """write time of parse data update"""
    conn.execute("INSERT INTO updates (stamp,ok) VALUES (?,?)", (datetime.datetime.now(), status))
    db.commit()


def get_last_update():
    """get time of last parse data update"""
    conn.execute("SELECT stamp FROM updates WHERE ok = 1 ORDER BY stamp DESC LIMIT 1")
    return datetime.datetime.strptime(conn.fetchone()[0], '%Y-%m-%d %H:%M:%S.%f')


def get_soup(wait=1):
    """если данные обновлены свежее, чем wait минут назад - взять с диска, иначе - парсить с сайта"""
    now_time = datetime.datetime.now()
    wait_time = datetime.timedelta(minutes=wait)
    if (now_time - get_last_update()) > wait_time:
        how_to_map = requests.get(
            'https://wiki.openstreetmap.org/wiki/RU:%D0%9A%D0%B0%D0%BA_%D0%BE%D0%B1%D0%BE%D0%B7%D0%BD'
            '%D0%B0%D1%87%D0%B8%D1%82%D1%8C').text  # страница, которую обрабатываем
        bs_soup = BeautifulSoup(how_to_map, 'lxml')
        with open("parse.html", "w", newline='', encoding="utf-8") as f:
            f.write(how_to_map)
        return bs_soup
    else:
        # read it back in
        with open("parse.html", newline='', encoding="utf-8") as f:
            bs_soup = BeautifulSoup(f, 'lxml')
        return bs_soup


def result_find(question):
    """это функция, которая находит раздел, уровень соответствия и содеражимое по запросу"""
    soup = get_soup()

    h3s = soup.find_all('h3')
    # тут вводится какое поиск мы делаем
    str2 = question
    matches = {}
    for i in h3s:
        str1 = i.text
        partial_ratio = fuzz.ratio(str1.lower(), str2.lower())
        matches[i.text] = (partial_ratio, i)

    x = sorted(matches, key=lambda k: matches[k][0], reverse=True)
    section, confidence = matches[x[0]][0], x[0]  # находим раздел

    position = h3s.index(matches[x[0]][1])

    text_content = []  # basic response
    for header in h3s[position:position + 1]:
        next_node = header
        while True:
            next_node = next_node.nextSibling
            if next_node is None:
                break
            if isinstance(next_node, bs4.NavigableString):
                text_content.append(next_node.strip())
            if isinstance(next_node, bs4.Tag):
                if next_node.name == "h3":
                    break
                text_content.append(next_node.get_text().strip())
    return confidence, section, ''.join(text_content)
