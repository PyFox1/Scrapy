import scrapy
from ..settings.settings import SPIDERS

class Spider4(scrapy.Spider):

    name = SPIDERS['spider4']['name']
    allowed_domains = SPIDERS['spider4']['allowed_domains']
    start_urls = SPIDERS['spider4']['start_url']

    def parse(self, response):
        counter = 0
        yield scrapy.Request(f'{SPIDERS["spider4"]["start_url"]}/?p={counter}', callback=self.parse_runs, meta={'counter': counter})

    def parse_runs(self, response):
        counter = response.request.meta['counter']
        if len(response.xpath('//div[@class="v-A_-appointment__entry__inner"]')) > 0:
            for run_info in response.xpath('//div[@class="v-A_-appointment__entry__inner"]'):
                yield {
                    "name": run_info.xpath(
                        './/span[@class="v-A_-headline v-A_-headline--gamma"]/text()').extract_first().strip(),
                    "distance": run_info.xpath('.//div[@class="v-A_-distance"]/span/text()').extract(),
                    "date": run_info.xpath('./div[@class="v-A_-appointment__entry__date"]/span/text()').extract(),
                    "location": run_info.xpath('.//span[@class="v-A_-location"]/text()').extract_first().strip(),

                }
            counter += 1
            yield scrapy.Request(f'{SPIDERS["spider4"]["start_url"]}/?p={counter}', callback=self.parse_runs, meta={'counter': counter})

