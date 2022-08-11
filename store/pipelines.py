# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from pymongo import MongoClient
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class StorePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.store

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['specification'] = self.process_spec(item['specification'])
        collection.insert_one(item)

        return item

    def process_spec(self, specification):
        raw_list = [elem.replace('\n', '').strip() for elem in specification]
        ready_list = [elem for elem in raw_list if elem]
        specification = dict(zip(ready_list[::2], ready_list[1::2]))
        return specification


class CastoramaImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['images'] = [itm[1] for itm in results if itm[0]]
        return item
