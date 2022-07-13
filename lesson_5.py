from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

options = Options()
options.add_argument("start-maximized")

s = Service(r'C:/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)

driver.get("https://pikabu.ru/")


for i in range(5):
    articles = driver.find_elements(By.TAG_NAME, 'article')
    actions = ActionChains(driver)
    actions.move_to_element(articles[-1])
    actions.perform()
    time.sleep(3)



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# import time
#
# s = Service('./chromedriver')
# driver = webdriver.Chrome(service=s)
#
# driver.get('https://gb.ru/login')
#
#
# login = driver.find_element(By.ID, 'user_email')
# login.send_keys("study.ai_172@mail.ru")
#
# pwd = driver.find_element(By.ID, 'user_password')
# pwd.send_keys("Password172")
#
# driver.execute_script('window.addEventListener("load", function(event) { console.log("All resources finished loading!"); });')
# submit = driver.find_element(By.CLASS_NAME, 'btn-success')
# try:
#     submit.click()
# except:
#     time.sleep(4)
#
# link = driver.find_element(By.XPATH, '//a[contains(@href, "/users/")]').get_attribute('href')
# driver.get(link)
#
# link = driver.find_element(By.CLASS_NAME, 'text-sm').get_attribute('href')
# driver.get(link)
#
# timezone = driver.find_element(By.NAME, 'user[time_zone]')
# select = Select(timezone)
# select.select_by_value('Rome')
# timezone.submit()
#


# pwd.send_keys(Keys.RETURN)
# time.sleep(1)

# driver.close()


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# import time
#
# s = Service('./chromedriver')
# driver = webdriver.Chrome(service=s)
#
# driver.get("https://www.atsenergo.ru/results/rsv/index")
# time.sleep(5)
# date = driver.find_element(By.ID, "aid_stats_1_date2")
# driver.execute_script("document.addEventListener('DOMContentLoaded', ready); ")