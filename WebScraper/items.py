# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import TakeFirst

class Advert(scrapy.Item):
    # define the fields for your item here like:
    Id = scrapy.Field(output_processor=TakeFirst())     # ID of advert
    Link = scrapy.Field(output_processor=TakeFirst())   # Link to advert
    Price = scrapy.Field()  # Price of flat or house
    NumberOfRooms = scrapy.Field(output_processor=TakeFirst())  # Number of rooms in house or apartment
    LivingAreaM2 = scrapy.Field(output_processor=TakeFirst())  # Living area in square meters
    LandAreaM2 = scrapy.Field(output_processor=TakeFirst())     # Whole area in square meters
    Age = scrapy.Field(output_processor=TakeFirst())    # Categorical new or older building
    Street = scrapy.Field(output_processor=TakeFirst())  # Street where estate is located
    City = scrapy.Field(output_processor=TakeFirst())  # Location of estate which we can later use for evaluation
    LastUpdate = scrapy.Field(output_processor=TakeFirst())  # Last update of advert
