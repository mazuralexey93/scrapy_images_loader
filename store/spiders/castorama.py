import scrapy
from scrapy.http import HtmlResponse
from store.items import StoreItem
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("query")}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[contains(@class, 'product-card__name')]")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=StoreItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@class='regular-price']/span/span/span//text()")
        loader.add_xpath('images', "//div[@class='js-zoom-container']/img/@data-src")
        loader.add_xpath('specification', "//div[contains(@class, 'product-specifications')]//dt//text() | //div[contains(@class, 'product-specifications')]//dd//text() ")
        loader.add_value('url', response.url)
        yield loader.load_item()
