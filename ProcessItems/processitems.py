import pymongo
import sys
import datetime

sys.path.append("..")

import config

date_now = datetime.datetime.now()
date = date_now.day + '/' + date_now.month + '/' + date_now.year

client = pymongo.MongoClient(config.MLAB_URI)

db = client['real_estate']

adv_coll = db['Adverts']
stats_coll = db['Stats_data']

for city in config.CITY_LIST:
    stats_coll.insert({'City': city[1], 'Date': date})

    for category in config.TYPE_CHOICES:
        # TODO go through all types and get statistics about those adverts into stats collection

# 1. Create new document: {'City': city, 'Date': date}
# 2. Insert stats for first category
    # db.test.update({ 'City' : city, 'Date': date }, { '$set': {Stats: [{'category': 1, 'Avg': Average, 'Min': Min}, {}]}})
# 3. Insert other categories
    # db.test.update({ 'City' : city, 'Date': date }, { '$push': {Stats: [{'category': 2, 'Avg': Average, 'Min': Min}, {}]}})

# http://stackoverflow.com/questions/26967525/insert-an-embedded-document-to-a-new-field-in-mongodb-document