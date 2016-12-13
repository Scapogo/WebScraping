import pymongo

client = pymongo.MongoClient('localhost', 27017)

db = client.RealEstate

collection = db.Adverts

print(collection.find().count())

for advert in collection.find():
    pass

# For deleting duplicate records in mongodb
# db.dups.aggregate([{$group:{_id:"$contact_id", dups:{$push:"$_id"}, count: {$sum: 1}}},
# {$match:{count: {$gt: 1}}}
# ]).forEach(function(doc){
#   doc.dups.shift();
#   db.dups.remove({_id : {$in: doc.dups}});
# });