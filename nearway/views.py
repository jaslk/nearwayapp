from django.shortcuts import get_object_or_404, render
from googleplaces import GooglePlaces, types, GooglePlacesError
from time import sleep
import numpy as np
import twitter
import csv
import xlwt
from django.http import Http404
# Create your views here.
from django.contrib.auth.models import User

from django.http import HttpResponse

from django.template import loader

MAX_FETCH = 10
YOUR_API_KEY = 'AIzaSyAutyhulLRnlnWms5bEQVys3e0kQPO5Fo8'
google_places = GooglePlaces(YOUR_API_KEY)

api = twitter.Api(consumer_key='jOwOxaedw3LF65HKDeHVjeFqK',
                  consumer_secret='mlcejDBraF0TQp47G481KZ9ZchhALi4gDIksoCKRYVQI47mfWM',
                  access_token_key='1047290727686950913-ELqL7KEZJIqiGhw7AqJCnTMy6uuqHZ',
                  access_token_secret='Bmj5vZdCoFPlZhUvIm3LNE4WE6mZuJoIZPhyucAwSXqHs')

sites_list = list()
lista_tipos = list()
direction = 0


def homepage(request):
    return render(request, 'nearway.html')


def twitter(request):
    return render(request, 'twitter.html')


def type_of_site(x, direction, radio=500):
    # ESTADIOS
    query_stadium = google_places.nearby_search(location=direction, radius=radio, types=[types.TYPE_STADIUM])
    # HOSPITALES
    query_hospital = google_places.nearby_search(location=direction, radius=radio, types=[types.TYPE_HOSPITAL])
    # IGLESIAS
    query_church = google_places.nearby_search(location=direction, radius=radio, types=[types.TYPE_CHURCH])
    # ESTACIÓN DE BUS
    query_bus_station = google_places.nearby_search(location=direction, radius=radio, types=[types.TYPE_BUS_STATION])
    # ESTACIÓN DE TREN
    query_train_station = google_places.nearby_search(location=direction, radius=radio,
                                                      types=[types.TYPE_TRAIN_STATION])
    #  ESTACIÓN DE TRÁNSITO
    # query_transit_station = google_places.nearby_search(location=direction, radius=1000,
    # types=[types.TYPE_TRANSIT_STATION])
    # COLEGIOS
    query_school = google_places.nearby_search(location=direction, radius=radio, types=[types.TYPE_SCHOOL])
    # UNIVERSIDADES
    query_university = google_places.nearby_search(location=direction, radius=radio, types=[types.TYPE_UNIVERSITY])
    # CEMENTERIO
    query_cemetery = google_places.nearby_search(location=direction, radius=radio, types=[types.TYPE_CEMETERY])
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


def icon_type(build_type):
    return {
        0: 'fa fa-soccer-ball-o fa-2x',
        1: 'fa fa-hospital-o fa-2x',
        2: 'fa fa-plus fa-2x',
        3: 'fa fa-bus fa-2x',
        4: 'fa fa-bus fa-2x',
        5: 'fa fa-graduation-cap fa-2x',
        6: 'fa fa-home fa-2x',
        7: 'fa fa-plus fa-2x',
    }[build_type]


def is_there(type_name):
    buildings = ['stadium', 'hospital', 'church', 'bus_station', 'school',
                 'university', 'cemetery', 'train_station']
    return type_name in buildings


def test(request):
    html = "nope"
    n = 8
    if 'buscar' in request.POST:
        global direction
        direction = request.POST.get('textfield', None)
        radio = request.POST.get('text_radio', None)
        checklist = np.zeros((8,), dtype=int)

        print("Este es el post: ", request.POST)

        for i in range(n):
            if str(i) in request.POST:
                checklist[i] = 1

        fetched = 0
        build_type = list()
        print(checklist)

        for i in range(len(checklist)):
            if checklist[i] == 1:
                number_type = i + 1

                type_site = type_of_site(number_type, direction, int(radio))
                for place in type_site.places:
                    if place:
                        place.get_details()

                        if is_there(place.details['types'][0]):
                            sites_list.append(place.name)
                            lista_tipos.append(place.details['types'][0])
                            build_type.append(icon_type(i))
                            print("BUILD TYPE:", build_type)
                            fetched = fetched + 1
                if type_site.has_next_page_token:
                    print('=========================================')
                    print('[NPT: %s]' % type_site.next_page_token)
                    print('=========================================')
                    query_stadium = google_places.nearby_search(
                        pagetoken=type_site.next_page_token)
                number_type += 1
            n = len(sites_list)
        return render(request, 'nearway.html',
                      context={'list': sites_list, 'direction': direction,
                               'build_type': build_type, 'type': lista_tipos, 'n': range(n)}, )
    else:
        return render(request, 'nearway.html')


def test_twitter(request):
    lista = list()
    if 'buscar' in request.POST:
        user = request.POST.get('textfield', None)

        results = api.GetSearch(raw_query="q=" + user + "%20&result_type=recent&count=100")

        for r in results:
            lista.append(r.text)

        n = len(lista)
        print("lista 1: ", lista)
        return render(request, 'twitter.html',
                      context={'list': lista, 'n': range(n), 'user': user}, )
    return render(request, 'twitter.html')


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="planilla.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sitios')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    ws.write(row_num, 0, 'Dirección', font_style)
    ws.write(row_num, 1, direction, font_style)

    row_num = 2
    columns = ['Sitio', 'Tipo de sitio']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for i in range(len(sites_list)):
        row_num += 1
        ws.write(row_num, 0, sites_list[i], font_style)
        ws.write(row_num, 1, lista_tipos[i], font_style)

    wb.save(response)
    return response
