# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath.
#
# Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

# Сложить собранные новости в БД
# Минимум один сайт, максимум - все три



print()
print('Задание 1')
print('________________________________________________________')
print()


from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint
import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.news_db  # База данных
db_collection = db.yandex # Коллекция

print('Делаем запрос...')
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
          }
url = 'https://yandex.ru/news'
session = requests.Session()
response = session.get(url, headers=header)
dom = html.fromstring(response.text)

news = []
sections = dom.xpath(".//section[@aria-labelledby]")
for section in sections:
    print('Работаем ...')

    section_title = section.xpath("@aria-labelledby")
    bloks = section.xpath(".//div[contains(@class,'mg-grid__item')]")

    for blok in bloks:
        blok_text = blok.xpath(".//h2[@class='mg-card__title']/a//text()")
        blok_link = blok.xpath(".//h2[@class='mg-card__title']/a//@href")
        blok_time = blok.xpath(".//span[@class='mg-card-source__time']/text()")
        now_timestamp = datetime.datetime.now()
        news_date = str(now_timestamp.date()) + ' ' + str(blok_time[0])


        count_search = len(list(db_collection.find({'news_link': blok_link[0]})))
        if count_search == 0:
            doc = {
                'section_title': section_title[0],
                'news_text': blok_text[0],
                'news_link': blok_link[0],
                'news_date': news_date,
                'news_source': 'https://yandex.ru/news'
            }
            db_collection.insert_one(doc)


#pprint(news)

print()
count_row_in_db = len(list(db_collection.find()))
print('Количество строк в базе: ', count_row_in_db)

print()
print('Первый попавшийся элемент в базе')
item = db_collection.find_one({})
pprint(item)

db_collection.drop()
print('End')