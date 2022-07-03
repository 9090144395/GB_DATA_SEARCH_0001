# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

print()
print('Задание 1')
print('________________________________________________________')
print()

import requests
import settings
import pprint
import json


token = settings.token
my_headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f'token {token}'
}

url = 'https://api.github.com/users/9090144395/repos'
response = requests.get(url, headers=my_headers)

if response.status_code == 200:
    print('Ответ на запрос получен: cтатус код 200')
    rezult = []
    repos_list = response.json()
    for item in repos_list:
        #print(item['name'])
        #pprint.pprint(item)
        name_repos = item['name']
        rezult.append(name_repos)

    print(f'Записываем результат в файл rezult.json')
    with open('rezult.json', 'w', encoding='utf-8') as file_out:
        json.dump(rezult, file_out)
else:
    print("Что то пошло не так (cтатус код не 200)")




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
print('Первое задание сделал с авторизацией')
print('При аутентификации в заголовке (X-RateLimit-Limit) видим лимит скорости (увеличился с 60 до 5000 запросов в час), что подтверждает успешность.')

# спека по авторизации
# https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps

# спека до методам
# https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user

print()
print('End')
