# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies1507


    def process_item(self, item, spider):
        item['salary'] = self.process_salary(item['salary'])
        temp = item
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        price = salary
        if price:
            if price[0] == "от " and price[2] == " до ":  # вариант ['от ', '200\xa0000', ' до ', '400\xa0000', ' ', 'руб.', ' ', 'до вычета налогов']
                job_price_min = str(price[1])
                job_price_min = int(job_price_min.replace('\xa0', ''))
                job_price_max = str(price[3])
                job_price_max = int(job_price_max.replace('\xa0', ''))
                job_price_currency = str(price[5])
            elif price[0] == "от ":  # вариант ['от ', '190\xa0000', ' ', 'руб.', ' ', 'на руки']
                job_price_min = str(price[1])
                job_price_min = int(job_price_min.replace('\xa0', ''))
                job_price_max = 0
                job_price_currency = str(price[3])
            elif price[0] == "до ":  # вариант ['до ', '210\xa0000', ' ', 'руб.', ' ', 'до вычета налогов']
                job_price_min = 0
                job_price_max = str(price[1])
                job_price_max = int(job_price_max.replace('\xa0', ''))
                job_price_currency = str(price[3])
            elif price[0] == 'з/п не указана':  # вариант ['з/п не указана']
                job_price_min = 0
                job_price_max = 0
                job_price_currency = 'не указано'
            else:  # вариант "150 000 – 250 000 руб."
                job_price_min_max = str(price[0]).split('–')
                job_price_min = int(job_price_min_max[0].replace('\u202f', ''))
                job_price_max = int(job_price_min_max[1].replace('\u202f', ''))
                job_price_currency = str(price[2])
        else:  # вариант "не указано"
            job_price_min = 0
            job_price_max = 0
            job_price_currency = 'не указано'


        return {'job_price_min': job_price_min, 'job_price_max': job_price_max, 'job_price_currency': job_price_currency}
