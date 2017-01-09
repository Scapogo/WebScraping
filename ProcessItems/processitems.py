import pymongo
import sys
import datetime
import numpy

sys.path.append("..")

import config

date_now = datetime.datetime.now()
date = date_now.day + '/' + date_now.month + '/' + date_now.year

client = pymongo.MongoClient(config.MLAB_URI)

db = client['real_estate']

adv_coll = db['Adverts']
stats_coll = db['Stats_data']


def getlist(adverts):
    pricelist = []

    for advert in adverts:
        pricelist.append(int(advert['Price'][0]))

    return pricelist


for city in config.CITY_LIST:
    stats_coll.insert({'City': city[1], 'Date': date})

    for category in config.TYPE_CHOICES:
        if category[0] == 1:
            adverts = adv_coll.find({'City': city[1], 'NumberOfRooms': category[0], 'House': 0}, {'Price': 1})

            pricelist = getlist(adverts)

            avg = sum(pricelist)/len(pricelist)
            min_price = min(pricelist)
            max_price = max(pricelist)
            med = numpy.median(pricelist)

            stats_coll.update({'City': city[1], 'Date': date}, {'set': {
                'Stats': [{'category': category[0], 'Avg': avg, 'Min': min_price, 'Max': max_price, 'Med': med}]}})
        elif category[0] < 5:
            adverts = adv_coll.find({'City': city[1], 'NumberOfRooms': category[0], 'House': 0}, {'Price': 1})

            pricelist = getlist(adverts)

            avg = sum(pricelist) / len(pricelist)
            min_price = min(pricelist)
            max_price = max(pricelist)
            med = numpy.median(pricelist)

            stats_coll.update({'City': city[1], 'Date': date}, {'$push': {
                'Stats': [{'category': category[0], 'Avg': avg, 'Min': min_price, 'Max': max_price, 'Med': med}]}})
        elif category[0] >= 5:
            adverts = adv_coll.find({'City': city[1], 'NumberOfRooms': category[0], 'House': 0}, {'Price': 1})

            pricelist = getlist(adverts)

            avg = sum(pricelist) / len(pricelist)
            min_price = min(pricelist)
            max_price = max(pricelist)
            med = numpy.median(pricelist)

            stats_coll.update({'City': city[1], 'Date': date}, {'$push': {
                'Stats': [{'category': category[0], 'Avg': avg, 'Min': min_price, 'Max': max_price, 'Med': med}]}})

        # TODO go through all types and get statistics about those adverts into stats collection

# 1. Create new document: {'City': city, 'Date': date}
# 2. Insert stats for first category
    # db.test.update({ 'City' : city, 'Date': date }, { '$set': {Stats: [{'category': 1, 'Avg': Average, 'Min': Min}, {}]}})
# 3. Insert other categories
    # db.test.update({ 'City' : city, 'Date': date }, { '$push': {Stats: [{'category': 2, 'Avg': Average, 'Min': Min}, {}]}})

# http://stackoverflow.com/questions/26967525/insert-an-embedded-document-to-a-new-field-in-mongodb-document