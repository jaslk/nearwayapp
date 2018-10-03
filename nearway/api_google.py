import googlemaps
from googleplaces import GooglePlaces, types, GooglePlacesError
from time import sleep
from django.shortcuts import render


def main(request):
    YOUR_API_KEY = 'AIzaSyAutyhulLRnlnWms5bEQVys3e0kQPO5Fo8'
    google_places = GooglePlaces(YOUR_API_KEY)

    direction = "Diosito"

    return render(request, 'test.html', context={'direction': direction},)


'''
def type_of_site(x):
    # ESTADIOS
    query_stadium = google_places.nearby_search(location=direction, radius=500, types=[types.TYPE_STADIUM])
    # HOSPITALES
    query_hospital = google_places.nearby_search(location=direction, radius=500, types=[types.TYPE_HOSPITAL])
    # IGLESIAS
    query_church = google_places.nearby_search(location=direction, radius=500, types=[types.TYPE_CHURCH])
    # ESTACIÓN DE BUS
    query_bus_station = google_places.nearby_search(location=direction, radius=500, types=[types.TYPE_BUS_STATION])
    # ESTACIÓN DE TREN
    query_train_station = google_places.nearby_search(location=direction, radius=500, types=[types.TYPE_TRAIN_STATION])
    #  ESTACIÓN DE TRÁNSITO
    # query_transit_station = google_places.nearby_search(location=direction, radius=1000,
    # types=[types.TYPE_TRANSIT_STATION])
    # COLEGIOS
    query_school = google_places.nearby_search(location=direction, radius=500, types=[types.TYPE_SCHOOL])
    # UNIVERSIDADES
    query_university = google_places.nearby_search(location=direction, radius=500, types=[types.TYPE_UNIVERSITY])
    # CEMENTERIO
    query_cemetery = google_places.nearby_search(location=direction, radius=500, types=[types.TYPE_CEMETERY])
    return {
        1: query_stadium,
        2: query_hospital,
        3: query_church,
        4: query_bus_station,
        5: query_train_station,
        # 6: query_transit_station,
        6: query_school,
        7: query_university,
        8: query_cemetery,
    }[x]


fetched = 0
number_type = 1
while number_type < 9:
    type_site = type_of_site(number_type)
    for place in type_site.places:
        if place:
            place.get_details()
            print('[%i] %s' % (fetched, place.name))
            print(place.geo_location)

            print(place.details['types'][0])
            fetched = fetched + 1
    if type_site.has_next_page_token:
        sleep(3)
        print('=========================================')
        print('[NPT: %s]' % type_site.next_page_token)
        print('=========================================')
        query_stadium = google_places.nearby_search(
            pagetoken=type_site.next_page_token)
    number_type += 1
'''
