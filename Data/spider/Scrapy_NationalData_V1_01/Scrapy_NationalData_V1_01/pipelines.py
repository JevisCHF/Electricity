# -*- coding: utf-8 -*-

import pymongo, logging

logger = logging.getLogger(__name__)


class MongoPipeline(object):
    collection_name = 'Energy_data'

    # collection_name = "test"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # self.db[self.collection_name].insert({'indic_name': item['indic_name']}, {'$set': item}, True)
        # return item

        if self.db[self.collection_name].count_documents(
                {
                    'indic_name': item['indic_name'],
                    'frequency': item['frequency'],
                    'data_year': item['data_year'],
                    'data_month': item['data_month'],
                    'data_day': item['data_day'],
                    'data_source': item['data_source'],
                    'region': item['region'],
                    'country': item['country'],
                    'data_value': item['data_value'],
                    "create_time": item["create_time"],
                }
        ) == 0:
            self.db[self.collection_name].insert(dict(item))
            return item['indic_name']
        else:
            err = 'the data is repetition .' + item['indic_name']
            logger.info(err)
            return None
