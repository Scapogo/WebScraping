import pymongo

client = pymongo.MongoClient('localhost', 27017)

db = client.RealEstate

collection = db.Adverts

print(collection.find().count())

for advert in collection.find():
    pass
