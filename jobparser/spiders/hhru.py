import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    list_url = []
    for industry_item in range(400):
        list_url.append(f'https://ekaterinburg.hh.ru/search/vacancy?industry={str(industry_item)}&search_field=name&search_field=company_name&search_field=description&text=python&items_on_page=100&no_magic=true&L_save_area=true')
    start_urls = list_url

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


        links = response.xpath("//div[@class='serp-item']//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)



    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@data-qa='vacancy-title']//text()").get()
        url = response.url
        price = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        yield JobparserItem(name=name, salary=price, url=url)




















