

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')

# Посмотрим список баз данных:
pprint(client.list_database_names())

# Создаём ссылку на базу данных testdb:
db = client.testdb  # База данных
fokus_collection = db.cars # Коллекция

cars = [
    {'name': 'Audi', 'price': 52642},
    {'name': 'Mercedes', 'price': 57127},
    {'name': 'Skoda', 'price': 9000},
    {'name': 'Volvo', 'price': 29000},
    {'name': 'Bentley', 'price': 350000},
    {'name': 'Citroen', 'price': 21000},
    {'name': 'Hummer', 'price': 41400}
         ]

db.cars.insert_many(cars)

doc = {'name': 'Volkswagen', 'price': 21600}
db.cars.insert_one(doc)


# посмотрим все коллекции в базе данных с именем testdb:
print(db.list_collection_names())

# возвращает курсор (НЕ СПИСОК), с помощью метода next мы можем идти по каждому элементу в переменной cars:
cars = db.cars.find()
print(cars.next())
print(cars.next())
print()

# С помощью метода list мы можем трансформировать курсор в список и работать уже со списком:
pprint(list(cars))
print()

# Количество элементов
n_cars = len(list(db.cars.find()))
print(n_cars)


print('----------------------------')
# Первый попавшийся элемент
item = fokus_collection.find_one({})
pprint(item)
print()

# поиск с элементом или
for item in fokus_collection.find({'$or':
                              [{'name': 'Audi'}, {'price': 21000}]
                            }):
    pprint(item)
print()

# поиск по значению
for item in fokus_collection.find({'name': 'Audi'}):
    pprint(item)
print()


# поиск с оператором сравнения
for item in fokus_collection.find({'price': {'$gte': 350000}}):  # >=55000
    pprint(item)
print()

# Условные операторы:
# $eq (равно)
# $ne (не равно)
# $gt (больше чем)
# $lt (меньше чем)
# $gte (больше или равно)
# $lte (меньше или равно)
# $in определяет массив значений, одно из которых должно иметь поле документа
# $nin определяет массив значений, которые не должно иметь поле документа

# поиск с регуляркой
for item in fokus_collection.find({'name': {'$regex': 'Au'}}):
    pprint(item)
print()


# Удалить коллекцию cars из базы данных testdb:
db.cars.drop()
print('----------------------------')



