# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность)
# с сайтов HH(обязательно) и/или Superjob(по желанию).
#
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# - Наименование вакансии.
# - Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# - Ссылку на саму вакансию.
# - Сайт, откуда собрана вакансия. (можно прописать статично hh.ru или superjob.ru)
#
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

print()
print('Задание 1')
print('________________________________________________________')
print()

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd

# спека bs4 https://beautiful-soup-4.readthedocs.io/en/latest/

session = requests.Session()
url = 'https://ekaterinburg.hh.ru/search/vacancy'

my_headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

job_data = {
    'job_name' : [],
    'job_href' : [],
    'job_site' : [],
    'job_price_min' : [],
    'job_price_max' : [],
    'job_price_currency' : []
}

have_next_page = True
number_page = 0
# будем перебирать страницы пока есть кнопка "Дальше"
while have_next_page:
    print(f'Делаю запрос на страницу {number_page}')
    my_params = {
        'text': 'python',
        'from': 'suggest_post',
        'fromSearchLine': 'true',
        'area': '3',
        'hhtmFrom': 'vacancy_search_list',
        'items_on_page': 20,
        # хм.. вывод по 100 на страницу не дает результатов
        # все равно находит только 20 штук в dom.find_all('div', {'class': 'vacancy-serp-item'})
        'page': number_page
    }

    response = session.get(url, params=my_params, headers=my_headers)

    if response.status_code == 200:
        print('Ответ на запрос получен: cтатус код 200')
        dom = BeautifulSoup(response.text, 'html.parser')

        # ищем вакансии
        my_tags_01 = dom.find_all('div', {'class': 'vacancy-serp-item'})
        #count_in_result_list = len(my_tags_01)

        for item in my_tags_01:
            # ищем описание в вакансии
            name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title', 'class': 'bloko-link', 'target': '_blank'})
            job_name = name.text
            href = name.get('href')
            job_data['job_name'].append(job_name)
            job_data['job_href'].append(href)
            job_data['job_site'].append('hh.ru')

            # ищем зп в вакансии
            price = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation', 'class': 'bloko-header-section-3'})
            if price:
                job_price = price.text
                temp = price.contents
                if price.contents[0] == "от ": # вариант "от 150 000 руб."
                    job_price_min = str(price.contents[2])
                    job_price_min = int(job_price_min.replace('\u202f',''))
                    job_price_max = 0
                    job_price_currency = str(price.contents[6])
                elif  price.contents[0] == "до ": # вариант "до 100 000 руб."
                    job_price_min = 0
                    job_price_max = str(price.contents[2])
                    job_price_max = int(job_price_max.replace('\u202f', ''))
                    job_price_currency = str(price.contents[6])
                else: # вариант "150 000 – 250 000 руб."
                    job_price_min_max = str(price.contents[0]).split('–')
                    job_price_min = int(job_price_min_max[0].replace('\u202f',''))
                    job_price_max = int(job_price_min_max[1].replace('\u202f',''))
                    job_price_currency = str(price.contents[2])

            else: # вариант "не указано"
                job_price_min = 0
                job_price_max = 0
                job_price_currency = 'не указано'

            job_data['job_price_min'].append(job_price_min)
            job_data['job_price_max'].append(job_price_max)
            job_data['job_price_currency'].append(job_price_currency)

        # проверяем, есть ли кнопка "Дальше"
        find_next_button = dom.find_all('a', {'class': 'bloko-button', 'data-qa':'pager-next'})
        if find_next_button:
            number_page += 1
        else:
            have_next_page = False

    else:
        print("Что то пошло не так (cтатус код не 200)")
        have_next_page = False

dataframe = pd.DataFrame(job_data)
dataframe.to_csv('result_hh_ru.csv', encoding='utf-8')

print('End')
