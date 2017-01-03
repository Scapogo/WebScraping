from django.shortcuts import render
import pymongo

from .forms import AdvertFilterForm

connection = pymongo.MongoClient('localhost', 27017)
db = connection.RealEstate
adverts_db = db.Adverts


def index(request):
    form = AdvertFilterForm()

    context = {'form': form}
    return render(request, 'estates/index.html', context)


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

    count, average = adverts_stats(adverts)

    context = {'average': average, 'count': count}
    return render(request, 'estates/senica.html', context)


def search(request):
    if request.method != 'POST':
        form = AdvertFilterForm()

        context = {'form': form}
        return render(request, 'estates/index.html', context)
    else:
        form = AdvertFilterForm(data=request.POST)
        if form.is_valid():
            selected = form.cleaned_data
            adverts = adverts_db.find({'City': 'Senica', 'NumberOfRooms': int(selected['estate_type'][0])},
                                      {'_id': 0, 'Id': 1, 'Price': 1,
                                       'Location': 1, 'NumberOfRooms': 1, 'Age': 1, 'LivingAreaM2': 1})
            count, average = adverts_stats(adverts)
        else:
            context = {'form': form}
            return render(request, 'estates/index.html', context)

    context = {'form': form, 'count': count, 'average': average, 'selected': selected}
    return render(request, 'estates/search.html', context)


def adverts_stats(adverts):
    """ Get statistics about selected adverts"""

    count = adverts.count()
    total = 0

    if count > 0:
        for advert in adverts:
            total += int(advert['Price'][0])

        average = total / count
    else:
        average = 0

    return count, average
