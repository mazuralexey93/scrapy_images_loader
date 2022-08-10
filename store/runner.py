from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from store.spiders.castorama import CastoramaSpider
from scrapy.utils.log import configure_logging

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    # query = input('Что ищем?: ')
    # runner.crawl(CastoramaSpider, query=query)

    runner.crawl(CastoramaSpider, query='мотоблок')
    # runner.crawl(CastoramaSpider, query='шланги')
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
