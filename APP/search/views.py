from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import format_html
from .serializers import ProductSerializer
import csv
import folium
from folium.plugins import FastMarkerCluster
from folium.plugins import MarkerCluster
import json

from app01.models import *


# Create your views here.
def models_api(request):
    brand = request.GET.get('brand')
    models = list(Piano.objects.filter(brand=brand))
    serializer = ProductSerializer(models, many=True)
    data = serializer.data
    options = []
    for model in models:
        option = f'<option value="{model.pid}">{model.model}</option>'
        options.append(option)
    response_data = {'models': data, 'options': options}
    
    return JsonResponse(response_data, safe=False)

def SearchFilterView(request):
    # for name search
    customers = User.objects.all()

    # for email
    emails = User.objects.values_list('email', flat=True)
    emails = list(map(str, emails))

    # for address search
    addresses = Address.objects.all()

    # for product search
    products = Piano.objects.values_list('brand', flat=True).distinct()
    products = list(map(str, products))

    # for model
    models = Piano.objects.all()

    if request.method == 'GET':

        autocomplete_name_query = request.GET.get('customer_name_auto')
        autocomplete_email_query = request.GET.get('customer_email')
        autocomplete_address_query = request.GET.get('auto_address')
        customer_phone_query = request.GET.get('customer_phone')
        autocomplete_product_query = request.GET.get('product_brand')
        product_type_query = request.GET.get('product_type')
        product_model_query = request.GET.get('product_submodel')
        tuning_date_query = request.GET.get('tuning_date')

        search_result = []

        customers_name = []
        customers_email = []
        customers_address_auto = []
        customers_phone = []
        customers_product = []
        customers_product_type = []
        customers_product_brand_and_type = []
        customers_product_model = []
        customers_product_brand_and_model = []
        customers_tuning = []
       

        # search from customer name
        if autocomplete_name_query != '' and autocomplete_name_query is not None:
            # your raw SQL query
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid WHERE concat_ws(' ',app01_user.first_name,app01_user.last_name) LIKE %s"
            # execute the raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(raw_query, [f'%{autocomplete_name_query}%'])
                results = cursor.fetchall()

            # create a list of dictionaries to store the results
            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_name.append(customer)
            customers_name = json.dumps(customers_name, default=str)    
            search_result.append(autocomplete_name_query)
        # search from customer email
        if autocomplete_email_query != '' and autocomplete_email_query is not None:
            # your raw SQL query
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid WHERE app01_user.email = %s"
            # execute the raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(raw_query, [autocomplete_email_query])
                results = cursor.fetchall()

            # create a list of dictionaries to store the results
            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_email.append(customer)
            customers_email = json.dumps(customers_email, default=str)
            search_result.append(autocomplete_email_query)
        # search from customer address,suburb,postcode
        if autocomplete_address_query != '' and autocomplete_address_query is not None:
            # your raw SQL query
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid WHERE concat_ws(' ',app01_address.address,app01_address.suburb,app01_address.postcode) LIKE %s ORDER BY app01_cpa.cid ASC"
            # execute the raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(raw_query, [f'%{autocomplete_address_query}%'])
                results = cursor.fetchall()

            # create a list of dictionaries to store the results
            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_address_auto.append(customer)
            customers_address_auto = json.dumps(customers_address_auto, default=str)
            search_result.append(autocomplete_address_query)
        # search from customer phone for exact match
        if customer_phone_query != '' and customer_phone_query is not None:
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid WHERE app01_user.phone_number = %s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [customer_phone_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_phone.append(customer)
            customers_phone = json.dumps(customers_phone, default=str)
            search_result.append(customer_phone_query)
        # search from piano brand
        if autocomplete_product_query != '' and autocomplete_product_query is not None and product_type_query == '0' and product_model_query == '0':
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid WHERE app01_piano.brand = %s" 

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [autocomplete_product_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_product.append(customer)
            customers_product = json.dumps(customers_product, default=str)
            search_result.append(autocomplete_product_query)
        # search from piano type
        if product_type_query != '0' and autocomplete_product_query == '' or autocomplete_product_query is None :
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid WHERE app01_piano.type = %s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [product_type_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_product_type.append(customer)
            customers_product_type = json.dumps(customers_product_type, default=str)
            search_result.append(product_type_query)
        # search from piano model
        if product_model_query != '' and product_model_query != '0' and autocomplete_product_query == '':
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid WHERE app01_piano.pid =%s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [product_model_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_product_model.append(customer)
            customers_product_model = json.dumps(customers_product_model, default=str)
            search_result.append(f'product ID: {product_model_query}')
        # search from piano brand and model
        if autocomplete_product_query != '' and product_model_query != '0':
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid WHERE app01_piano.brand =%s and app01_piano.pid =%s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [autocomplete_product_query,product_model_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_product_brand_and_model.append(customer)
            customers_product_brand_and_model = json.dumps(customers_product_brand_and_model, default=str)
            search_result.append(f'{autocomplete_product_query,product_model_query}')
        # search from piano and type
        if autocomplete_product_query != '' and product_type_query != '0':
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid WHERE app01_piano.brand =%s and app01_piano.type = %s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [autocomplete_product_query,product_type_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_product_brand_and_type.append(customer)
            customers_product_brand_and_type = json.dumps(customers_product_brand_and_type, default=str)
            search_result.append(f'{autocomplete_product_query,product_type_query}')

        # search from last tuning date
        if tuning_date_query != '0' and tuning_date_query != '':
            raw_query = "select app01_cpa.cid, app01_user.first_name, app01_user.last_name, app01_user.email, app01_user.phone_number, app01_address.address, app01_address.suburb, app01_address.postcode, app01_piano.brand, app01_piano.model, app01_piano.type, app01_address.lat, app01_address.long, app01_address.aid from app01_cpa cross join app01_user on app01_cpa.cid = app01_user.uid cross join app01_address on app01_cpa.aid_id = app01_address.aid cross join app01_piano on app01_cpa.pid_id = app01_piano.pid cross join app01_tuning on app01_cpa.cid = app01_tuning.cid_id WHERE app01_tuning.tuning_date < DATE_SUB(NOW(), INTERVAL %s MONTH)"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [tuning_date_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': str(row[11]), 
                    'longitude': str(row[12]),
                    'aid': row[13]
                }
                customers_tuning.append(customer)
            customers_tuning = json.dumps(customers_tuning, default=str)
            search_result.append(tuning_date_query)

        # combine lists
        unique_result = []

        def parse_json_or_null(x):
            try:
                return json.loads(x)
            except:

                return None

        _search_results = [
            customers_phone,
            customers_address_auto,
            customers_product,
            customers_name,
            customers_email,
            customers_product_type,
            customers_product_brand_and_type,
            customers_product_model,
            customers_product_brand_and_model,
            customers_tuning
        ]

        for s in _search_results:
            _s = parse_json_or_null(s)
            if _s is not None:
                unique_result.extend(_s)
        # unique_result.extend(json.loads(customers_phone))
        # unique_result.extend(json.loads(customers_address_auto))
        # unique_result.extend(json.loads(customers_product))
        # unique_result.extend(json.loads(customers_name))
        # unique_result.extend(json.loads(customers_email))
        # unique_result.extend(json.loads(customers_product_type))
        # unique_result.extend(json.loads(customers_product_brand_and_type))
        # unique_result.extend(json.loads(customers_product_model))
        # unique_result.extend(json.loads(customers_product_brand_and_model))
        # unique_result.extend(json.loads(customers_tuning))

        # unique_result += [customers_address_auto]
        # unique_result += [customers_product]
        # unique_result += [customers_name]
        # unique_result += [customers_email]
        # unique_result += [customers_product_type]
        # unique_result += [customers_product_brand_and_type]
        # unique_result += [customers_product_model]
        # unique_result += [customers_product_brand_and_model]
        # unique_result += [customers_tuning]

        print("unique_result",unique_result)
        # remove duplicates
        # unique_result = [dict(t) for t in {tuple(d.items()) for d in unique_result}]
        # retrieve search result from session
        request.session['search_result'] = unique_result

        # map visualization
        customer_house = request.session.get('search_result', [])
        print("customer_house",customer_house)
        if customer_house =='[]':
            # set customer_house to 1 if no search result for map remain on the page
            customer_house = 1
        else:
            # create Folium map randomly centered 
            mapdisplay = folium.Map(location=[-37.8136, 144.9631], zoom_start=10)
            # marker_cluster = MarkerCluster()
            # latitude_map = []
            # longitude_map = []
            # print(customer_house[0])
            # customer_house = json.loads(customer_house[0])
            # add markers for all houses
            for house in customer_house:
                house_id = house['aid']
                location = list(Address.objects.filter(aid=house_id))
                
                for address in location:
                    latitude = address.lat
                    longitude = address.long
                    address = location[0].address
                    suburb = location[0].suburb
                    postcode = location[0].postcode

                    # latitude_map.append(latitude)
                    # longitude_map.append(longitude)
                    
                    # format the address as a string with a tooltip prefix
                    tooltip_text = "Address: {} {} {}".format(address, suburb, postcode)

                    # single marker
                    coordinates = (latitude, longitude)
                    folium.Marker(coordinates, popup=tooltip_text).add_to(mapdisplay)
                    # marker = folium.Marker(location=[latitude, longitude], popup=tooltip_text)
                    # add the marker to the MarkerCluster
                    # marker_cluster.add_child(marker)

            # add the MarkerCluster to the map
            # mapdisplay.add_child(marker_cluster)
            # convert map to html
            m = mapdisplay._repr_html_()

    return render(request, 'search.html', {'searched':search_result,'customers': unique_result,'names':customers,'emails':emails, 'addresses': addresses,'products':products,'models':models,'nbar': 'search','map_html':m})

def export_csv(request):
        # retrieve search results
        results_list = request.session.get('search_result', [])
        # create the HttpResponse object with CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="search_results.csv"'

        # create a writer object for CSV
        writer = csv.writer(response)

        # write the header row
        writer.writerow(['cid', 'first_name', 'last_name', 'email', 'phone', 'address', 'suburb', 'postcode', 'brand', 'model', 'type'])

        # write the data rows
        for result in results_list:
            writer.writerow([result['id'], result['first_name'], result['last_name'], result['email'], result['phone'], result['address'], result['suburb'], result['postcode'], result['brand'], result['model'], result['type']])

        return response

# for map.html
def MapView(request):

    return render(request, 'map.html', {'nbar': 'map'})

def DashbordView(request):
    # map visualization for all customer 
    locations = Address.objects.all()
    mapdisplay = folium.Map(location=[-37.8136, 144.9631], zoom_start=10)

    latitude = [location.lat for location in locations]
    longitude = [location.long for location in locations]

    FastMarkerCluster(data=list(zip(latitude, longitude))).add_to(mapdisplay)
    # convert map to html
    m = mapdisplay._repr_html_()

    return render(request, 'dashboard.html', {'nbar': 'dashboard','map_dashboard':m})
