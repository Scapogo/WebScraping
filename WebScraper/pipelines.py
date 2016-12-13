# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
#  from scrapy import log


class WebscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))

        if valid:
            item_id = str(item['Id'][0])
            if self.collection.find_one({'Id': item_id}) == None:
                try:
                    self.collection.insert(dict(item))
                    print("Added to mongodb: " + str(item['Id']))
                except:
                    print("Failed to write into mongodb")
                # log.msg("Question added to MongoDB database!",
                #         level=log.DEBUG, spider=spider)
            else:
                try:
                    response = self.collection.find_one({"Id": item_id}, {'_id': 0, 'Price': 1, 'LastUpdate': 1})

                    if item['LastUpdate'][0] == response['LastUpdate'][0]:
                        return
                    else:
                        prices = response['Price']
                        for price in prices:
                            item['Price'].append(price)

                        print("Prices: " + item['Price'][0])

                        self.collection.update_one({'Id': item_id}, {'$set': {'Price': item['Price'],
                                                                              'LastUpdate': item['LastUpdate']}}
                                                   , upsert=False)

                        print("Updated item in mongodb: " + str(item['Id']))
                except Exception as inst:
                    print("Failed to write into mongodb" + inst)
        return item
