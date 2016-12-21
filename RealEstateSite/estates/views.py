from django.shortcuts import render
import pymongo

connection = pymongo.MongoClient('localhost', 27017)
db = connection.RealEstate
adverts_db = db.Adverts


def index(request):
    return render(request, 'estates/index.html')


def senica(request):

    adverts = adverts_db.find({'City': 'Senica'}, {'_id': 0, 'Id': 1, 'Price': 1, 'Location': 1,
                                               'NumberOfRooms': 1, 'Age': 1, 'LivingAreaM2': 1})

    count = adverts.count()
    total = 0

    for advert in adverts:
        total += int(advert['Price'][0])

    average = total/count

    context = {'average': average, 'count': count}
    return render(request, 'estates/senica.html', context)


def senica_room_filter(request, room_number):
    adverts = adverts_db.find({'City': 'Senica', 'NumberOfRooms': int(room_number)}, {'_id': 0, 'Id': 1, 'Price': 1,
                                            'Location': 1, 'NumberOfRooms': 1, 'Age': 1, 'LivingAreaM2': 1})

    count = adverts.count()
    total = 0

    if count > 0:
        for advert in adverts:
            total += int(advert['Price'][0])

        average = total / count
    else:
        average = 0

    context = {'average': average, 'count': count}
    return render(request, 'estates/senica.html', context)
