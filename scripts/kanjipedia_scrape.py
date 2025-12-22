import requests
import re
from bs4 import BeautifulSoup

url = "https://www.kanjipedia.jp/kanji/0000138600"
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, "lxml")

yomi_list = soup.find('ul', id='onkunList')

print(yomi_list)
readings = yomi_list.find_all('p', class_='onkunYomi')

print(yomi_list)
print(readings)
for reading in readings:
    print("-------")
    print(reading)
    stripped = re.sub(r'<[^>]*>', '', str(reading))
    converted = re.sub(r'・', '/', stripped)
    print(converted)