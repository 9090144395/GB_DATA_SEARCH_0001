# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии/продукты в вашу базу.


from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')

# Посмотрим список баз данных:
pprint(client.list_database_names())

# Создаём ссылку на базу данных testdb:
db = client.testdb  # База данных

cars = [ {'name': 'Audi', 'price': 52642},
    {'name': 'Mercedes', 'price': 57127},
    {'name': 'Skoda', 'price': 9000},
    {'name': 'Volvo', 'price': 29000},
    {'name': 'Bentley', 'price': 350000},
    {'name': 'Citroen', 'price': 21000},
    {'name': 'Hummer', 'price': 41400},
    {'name': 'Volkswagen', 'price': 21600} ]

db.cars.insert_many(cars)
db.cars # Коллекция

#Теперь посмотрим все коллекции в базе данных с именем testdb:
print(db.list_collection_names())

# возвращает курсор, с помощью метода next мы можем идти по каждому элементу в переменной cars:
cars = db.cars.find()
print(cars.next())
print(cars.next())
print()

# С помощью метода list мы можем трансформировать курсор в список и работать уже со списком:
pprint(list(cars))
print()

n_cars = len(list(db.cars.find()))
print(n_cars)



fokus_collection = db.cars
item = fokus_collection.find_one({})
pprint(item)
print()


for item in fokus_collection.find({'$or':
                              [
                                {'name': 'Audi'},
                                {'price': 21000}
                               ]
                            }):
    pprint(item)

print()

for item in fokus_collection.find({'name': 'Audi'}):
    pprint(item)

print()



# for item in persons.find({'age': {'$gte': 29}}):
#     pprint(item)
#
# for item in persons.find({'author': {'$regex': '^Pet$'}}):
#     pprint(item)


# Удалить коллекцию cars из базы данных testdb:
db.cars.drop()
print('----------------------------')

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты). То есть цифра вводится одна, а запрос проверяет оба поля


