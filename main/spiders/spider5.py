import scrapy
from ..settings.settings import SPIDERS


class Spider5(scrapy.Spider):
    name = SPIDERS['spider5']['name']
    allowed_domains = SPIDERS['spider5']['allowed_domains']
    start_urls = SPIDERS['spider5']['start_url']


    def parse(self, response):
        for run_info in response.xpath('.//div[@id="divContentList"]//tr'):

            date_default = run_info.xpath('normalize-space(.//div[@class="divContentList1stClmn"]/a/text())').get().replace(u'\xa0', u'')
            if date_default:
                date = date_default
            else:
                date = ''.join(run_info.xpath('.//span[@class="spanDatumVonBis"]/text()').getall())

            name = run_info.xpath('normalize-space(.//h3/a/text())').get(),
            location = run_info.xpath('normalize-space(.//td/div[@class="divContentListlastClmn"]/a/text())')[0].get(),
            url = run_info.xpath('.//h3/a/@href').get()

            if url:
                yield scrapy.Request(url, self.parse_sub, meta={'date': date, 'name': name, 'location': location})

        next_page = response.xpath('.//td[3]/a[@class="shsLink"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_sub(self, response):

        event = response.xpath('//div[@id="divContentDetailMarathonIcons"]//img/@title').getall()

        yield {
                'date': response.request.meta['date'],
                'name': response.request.meta['name'],
                'location': response.request.meta['location'],
                'country_list': response.xpath('.//div[@class="divContentDetailMarathonDetailInfos"]//tr[1]//td[2]/text()').getall(),
                'event': event,
                'website': response.xpath('normalize-space(//div[@class="divContentDetailLBInfoBlockImgs"]//a[1]/@href)').get()
        }