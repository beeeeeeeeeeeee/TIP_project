from django.shortcuts import render
from django.http import Http404
from django.conf import settings

import folium
from folium.plugins import FastMarkerCluster
from folium.plugins import MarkerCluster

from .models import Suburb

import environ

env = environ.Env()

# Create your views here.

def index(request):
    suburb_list = Suburb.objects.order_by('id')
    template = 'suburb_finder/index.html'
    context = {
        'suburb_list': suburb_list,
        'api_key': settings.GOOGLE_API_KEY,
        'nbar' : 'suburb_finder',
    }
    
    google_api = env("GOOGLE_API_KEY")
    
    return render(request, template, context)

def detail(request, suburb_id):
    # show list of customers in suburb
    
    
    try:
        suburb = Suburb.objects.get(pk=suburb_id)
    except Suburb.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'suburb_finder/detail.html', {'suburb': suburb})

def DashbordView(request):
    # map visualization for all customer 
    #locations = Address.objects.all()
    mapdisplay = folium.Map(location=[-37.8136, 144.9631], zoom_start=10)
    
    

    #latitude = [location.lat for location in locations]
    #longitude = [location.long for location in locations]

    #FastMarkerCluster(data=list(zip(latitude, longitude))).add_to(mapdisplay)
    # convert map to html
    m = mapdisplay._repr_html_()
    
    context = {
        'api_key': settings.GOOGLE_API_KEY,
        'nbar': 'dashboard',
        'map_dashboard': m,
        'nbar' : 'dashboard',
    }
    template = 'suburb_finder/dashboard.html'

    return render(request, template, context)

