from django.shortcuts import render
import pymongo

from .forms import AdvertFilterForm

connection = pymongo.MongoClient('localhost', 27017)
db = connection.RealEstate
adverts_db = db.Adverts
CITY_LIST = (('0', 'Senica'), ('1', 'Skalica'))

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
    """ Return web page which shows data based on form data"""

    if request.method != 'POST':
        # Redirect to index web page if there are no POSTED data
        form = AdvertFilterForm()

        context = {'form': form}
        return render(request, 'estates/index.html', context)
    else:
        form = AdvertFilterForm(data=request.POST)
        if form.is_valid():
            selected = form.cleaned_data    # for debug purposes, should be removed later
            city = CITY_LIST[int(form.cleaned_data['city'])][1]  # get selected city from form

            # look for selected sizes of house/appartments
            estate_types = []
            for item in form.cleaned_data['estate_type']:
                estate_types.append(int(item[0]))

            adverts = adverts_db.find({'City': city, 'NumberOfRooms': {'$in': estate_types}},
                                      {'_id': 0, 'Id': 1, 'Price': 1,
                                       'Location': 1, 'NumberOfRooms': 1, 'Age': 1, 'LivingAreaM2': 1})
            # TODO Make this query more dynamical so it can work even if no room number is selected

            count, average = adverts_stats(adverts)  # get statistical information
        else:
            # is submitted form is not valid return to index page
            context = {'form': form}
            return render(request, 'estates/index.html', context)

    context = {'form': form, 'count': count, 'average': average, 'selected': selected, 'city': city}
    return render(request, 'estates/search.html', context)


def adverts_stats(adverts):
    """ Get statistics about selected adverts"""
    # TODO Add more statistics and probably convert return into tuple or dictionary

    count = adverts.count()
    total = 0

    if count > 0:
        for advert in adverts:
            total += int(advert['Price'][0])

        average = total / count
    else:
        average = 0

    return count, average
