from django.shortcuts import render
from django.http import Http404
from django.conf import settings

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

