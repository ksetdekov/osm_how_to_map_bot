from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from lxml.html.clean import unicode

how_to_map = requests.get('https://wiki.openstreetmap.org/wiki/RU:%D0%9A%D0%B0%D0%BA_%D0%BE%D0%B1%D0%BE%D0%B7%D0%BD'
                          '%D0%B0%D1%87%D0%B8%D1%82%D1%8C').text
soup = BeautifulSoup(how_to_map, 'lxml')
h3s = soup.find_all('h3')
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
# todo сохранить файл и перечитывать его раз в минуту


print(soup.find('h3').next_sibling)

with open("A.txt", "w", newline='', encoding="utf-8") as f:
    f.write(how_to_map)

# read it back in
with open("A.txt", newline='', encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'lxml')
    # do something with soup


