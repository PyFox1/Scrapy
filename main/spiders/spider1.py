# -*- coding: utf-8 -*-
import scrapy
from ..settings.settings import SPIDERS


class Spider1(scrapy.Spider):
    name = SPIDERS['spider1']['name']
    allowed_domains = SPIDERS['spider1']['allowed_domains']
    start_urls = SPIDERS['spider1']['start_url']

    def parse(self, response):
        rows = response.xpath('//body/table[2]//tr')
        for row in rows:
            date = row.xpath('normalize-space(.//td[1]/text())').get()
            name = row.xpath('normalize-space(.//td[2]/a/text())').get()
            url = row.xpath('.//td[2]/a/@href').get()
            if date and name:
                absolute_url = response.urljoin(url)
                yield scrapy.Request(absolute_url, self.get_sub_url, meta={'name': name, 'sub_url': url})

    def get_sub_url(self, response):
        address = response.xpath('//div[@class="lk-adr"][position() > 1]/text()').getall()
        distances = response.xpath('//div[@class="lk-renn"][position() > 1]/text()').getall()
        result_list = response.xpath('//div[@class="lk-ergb"][position() > 1]/text()').getall()
        date = response.xpath('//div[@class="lk-dat"]/text()').get()
        yield {
            'date': date,
            'name': response.request.meta['name'],
            'distance': distances,
            'address': address,
            'result_list': result_list
        }

