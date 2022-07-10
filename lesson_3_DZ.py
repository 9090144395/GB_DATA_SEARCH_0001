# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии/продукты в вашу базу.


print()
print('Задание 1')
print('________________________________________________________')
print()

import pandas as pd
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client.hh_db  # База данных
db_collection = db.cars # Коллекция

# читаем файл, который сохранили на прошлом задании
print('Читаем файл')
dataframe = pd.read_csv('result_hh_ru.csv', encoding='utf-8')
count_row_in_dataframe = len(dataframe.index)
print('Количество строк в файле: ', count_row_in_dataframe)
print()


generator = (
    (job_href, job_name, job_site, job_price_min, job_price_max, job_price_currency)
    for job_href, job_name, job_site, job_price_min, job_price_max, job_price_currency
    in zip(
    dataframe['job_href'],
    dataframe['job_name'],
    dataframe['job_site'],
    dataframe['job_price_min'],
    dataframe['job_price_max'],
    dataframe['job_price_currency']
    )
)

print('Обновляем данные в базе ...')
for item_job_href, item_job_name, item_job_site, item_job_price_min, item_job_price_max, item_job_price_currency in generator:
    temp_1 = item_job_href
    # у каждой вакансии уникальной является ссылка
    # поиск по ссылке и количество найденных
    count_search = len(list(db_collection.find({'job_href': item_job_href})))
    if count_search == 0:
        doc = {
            'job_href': item_job_href,
            'job_name': item_job_name,
            'job_site': item_job_site,
            'job_price_min': item_job_price_min,
            'job_price_max': item_job_price_max,
            'job_price_currency': item_job_price_currency
        }
        db_collection.insert_one(doc)


print()
count_row_in_db = len(list(db_collection.find()))
print('Количество строк в базе: ', count_row_in_db)

print()
print('Первый попавшийся элемент в базе')
item = db_collection.find_one({})
pprint(item)


# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты). То есть цифра вводится одна, а запрос проверяет оба поля


print()
print('Задание 2')
print('________________________________________________________')
print()

print('Поиск вакансий, в которых стоимость более 100 000..')
def search_in_db(price):
    condition = {'$gte': price}
    search = db_collection.find(
        {
        '$and':
        [{'job_price_min': condition}, {'job_price_max': condition}]
        }
    )
    for item_search in search:
        pprint(item_search)

    return search


for item_search in search_in_db(100000):
    pprint(item_search)


# Условные операторы задают условие, которому должно соответствовать значение поля документа:
# $eq (равно)
# $ne (не равно)
# $gt (больше чем)
# $lt (меньше чем)
# $gte (больше или равно)
# $lte (меньше или равно)
# $in определяет массив значений, одно из которых должно иметь поле документа
# $nin определяет массив значений, которые не должно иметь поле документа