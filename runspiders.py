import os, sys


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from main.spiders.all_spiders import SPIDERS


# change root path of scrapy settings file
settings_file_path = 'main.settings.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

# add flask project to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# start crawler
process = CrawlerProcess(settings=get_project_settings())
process.crawl(SPIDERS['Spider5'])

if __name__ == '__main__':
    process.start()


