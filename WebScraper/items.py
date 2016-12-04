# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Advert(scrapy.Item):
    # define the fields for your item here like:
    Id = scrapy.Field()     # ID of advert
    Link = scrapy.Field()   # Link to advery
    Price = scrapy.Field()  # Price of flat or house
    NumberOfRooms = scrapy.Field()
    LivingAreaM2 = scrapy.Field()  # Living area in square meters
    LandAreaM2 = scrapy.Field()     # Whole area in square meters
    Age = scrapy.Field()    # Categorical new or older building
    Location = scrapy.Field()
    LastUpdate = scrapy.Field()  # Last update of advert
