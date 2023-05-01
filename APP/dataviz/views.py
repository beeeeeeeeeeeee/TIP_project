from django.shortcuts import render

# Create your views here.

# Path: APP/dataviz/views.py
#dummy view
def index(request):

    return render(request, 'index/index.html',{})
