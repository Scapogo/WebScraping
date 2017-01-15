import pymongo
import sys
import datetime
import numpy

sys.path.append("..")

import config

date_now = datetime.datetime.now()
date = str(date_now.day) + '/' + str(date_now.month) + '/' + str(date_now.year)

client = pymongo.MongoClient(config.MLAB_URI)

db = client['real_estate']

adv_coll = db['Adverts']
stats_coll = db['Stat_data']


def getlist(adverts):
    """Get only latest prices from adverts, make list out of them for easier processing later"""

    pricelist = []

    for advert in adverts:
        # print(advert['Price'][0])  # Just for debuging purposes
        pricelist.append(int(advert['Price'][0]))

    return pricelist


def getstats(pricelist):
    """Get statistical information about prices"""

    if len(pricelist) > 0:
        # Get average, min, max, median price of adverts for category
        count = len(pricelist)
        average = sum(pricelist) / count
        min_price = min(pricelist)
        max_price = max(pricelist)
        median = numpy.median(pricelist)

        return average, min_price, max_price, median, count
    else:
        return 0, 0, 0, 0, 0


for city in config.CITY_LIST:
    stats_coll.insert({'City': city[1], 'Date': date_now})

    for category in config.TYPE_CHOICES:
        print(category[0])  # Just for debuging purposes
        if int(category[0]) == 1:
            adverts = adv_coll.find({'City': city[1], 'NumberOfRooms': int(category[0]), 'House': 0}, {'Price': 1})

            pricelist = getlist(adverts)

            avg, min_price, max_price, med, count = getstats(pricelist)

            stats_coll.update({'City': city[1], 'Date': date_now}, {'$set': {
                'Stats': [{'category': category[0], 'Avg': avg, 'Min': min_price, 'Max': max_price, 'Med': med,
                           'Count': count}]}})
        elif int(category[0]) < 5:
            adverts = adv_coll.find({'City': city[1], 'NumberOfRooms': int(category[0]), 'House': 0}, {'Price': 1})

            pricelist = getlist(adverts)

            avg, min_price, max_price, med, count = getstats(pricelist)

            stats_coll.update({'City': city[1], 'Date': date_now}, {'$push': {
                'Stats': {'category': category[0], 'Avg': avg, 'Min': min_price, 'Max': max_price, 'Med': med,
                           'Count': count}}})
        elif int(category[0]) == 5:
            adverts = adv_coll.find({'City': city[1], 'House': 1}, {'Price': 1})

            pricelist = getlist(adverts)

            avg, min_price, max_price, med, count = getstats(pricelist)

            stats_coll.update({'City': city[1], 'Date': date_now}, {'$push': {
                'Stats': {'category': category[0], 'Avg': avg, 'Min': min_price, 'Max': max_price, 'Med': med,
                           'Count': count}}})
        elif int(category[0]) == 6:
            adverts = adv_coll.find({'City': city[1], 'Land': 1}, {'Price': 1})

            pricelist = getlist(adverts)

            avg, min_price, max_price, med, count = getstats(pricelist)

            stats_coll.update({'City': city[1], 'Date': date_now}, {'$push': {
                'Stats': {'category': category[0], 'Avg': avg, 'Min': min_price, 'Max': max_price, 'Med': med,
                           'Count': count}}})

# 1. Create new document: {'City': city, 'Date': date}
# 2. Insert stats for first category
    # db.test.update({ 'City' : city, 'Date': date }, { '$set': {Stats: [{'category': 1, 'Avg': Average, 'Min': Min}, {}]}})
# 3. Insert other categories
    # db.test.update({ 'City' : city, 'Date': date }, { '$push': {Stats: [{'category': 2, 'Avg': Average, 'Min': Min}, {}]}})

# http://stackoverflow.com/questions/26967525/insert-an-embedded-document-to-a-new-field-in-mongodb-document