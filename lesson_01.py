# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

print()
print('Задание 1')
print('________________________________________________________')
print()

import requests
import settings

# get started
token = settings.token
url = 'https://api.github.com/users/9090144395'
response = requests.get(url)

if response.status_code == 200:
    profile_data = response.json()
else:
    print("Что то пошло не так - статус код не 200")


# 2. Изучить список открытых API
# (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
# Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.
#

print()
print('Задание 2')
print('________________________________________________________')
print()




