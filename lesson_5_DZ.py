# Вариант II
# Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
# Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары

print()
print('Задание (выбрал второй вариант)')
print('________________________________________________________')
print()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client.mvideo_db  # База данных
db_collection = client.mvideo_db.in_trend # Коллекция


options = Options()
options.add_argument("start-maximized")
s = Service(r'C:/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)
driver.get("https://www.mvideo.ru/")
time.sleep(1)


scrolling_position = 0
while True:
    try:
        # пробуем найти кнопку
        button_in_trend = driver.find_element(By.XPATH, ".//span[contains(text(),'В тренде')]/../..")
        button_in_trend.click()
        # немного проскролим вниз для удобства
        scrolling_position += 300
        driver.execute_script(f"window.scrollTo(0, {scrolling_position})")
        time.sleep(1)
        break
    except NoSuchElementException:
        # скролл, если попытка найти не удалась
        scrolling_position += 100
        driver.execute_script(f"window.scrollTo(0, {scrolling_position})")
        # driver.sendKeys(Keys.PAGE_DOWN) #  альтернатива скроллингу
        time.sleep(1)


print()

# Ищем карусель и перебироаем карточки с товарами ...
cards_in_trend = driver.find_elements(By.XPATH, "//mvid-shelf-group//mvid-product-cards-group//div[@class='title']")
for card in cards_in_trend:
    name = card.text
    #print(name)
    link = card.find_element(By.XPATH, "./a").get_attribute('href')
    #print(link)

    # ищем в базе элементы идобавляем если их нет
    count_search = len(list(db_collection.find({'link_to_product': link})))
    if count_search == 0:
        doc = {
            'name_product': name,
            'link_to_product': link,
            'group_product': 'In trend',
            'source': 'https://www.mvideo.ru/'
        }
        db_collection.insert_one(doc)

driver.close()

print()
count_row_in_db = len(list(db_collection.find()))
print('Количество строк в базе: ', count_row_in_db)

print()
item = db_collection.find_one({})
print('Первый попавшийся элемент в базе')
pprint(item)

# очищаем базу для тестирования
db_collection.drop()
print('End')
