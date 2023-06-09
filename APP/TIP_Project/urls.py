"""TIP_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include

from app01 import views
from suburb_finder.views import DashbordView
from dataviz import views as dataviz_views
from suburb_finder import views as suburb_finder_views

from search.views import SearchFilterView, models_api, export_csv, MapView, DashbordView

urlpatterns = [

    path("suburb_finder/", suburb_finder_views.index, name = 'suburb_finder'),
    path("", suburb_finder_views.index, name = 'suburb_finder'),

    path("admin/", admin.site.urls),
    
    path("address/list/", views.address_list, name="data_management"),
    path("address/add/", views.address_add),
    path("address/<int:nid>/edit/", views.address_edit),
    path("address/multi/", views.address_multi),
    path("address/delete/", views.address_delete),
    #

    path("piano/list/", views.piano_list),
    path("piano/add/", views.piano_add),
    path("piano/<int:nid>/edit/", views.piano_edit),
    path("piano/multi/", views.piano_multi),
    path("piano/delete/", views.piano_delete),

    path("user/list/", views.user_list),
    path("user/add/", views.user_add),
    path("user/<int:nid>/edit/", views.user_edit),
    path("user/multi/", views.user_multi),
    path("user/delete/", views.user_delete),

    path("cpa/list/", views.cpa_list),
    path("cpa/add/", views.cpa_add),
    path("cpa/<int:nid>/edit/", views.cpa_edit),
    path("cpa/multi/", views.cpa_multi),
    path("cpa/delete/", views.cpa_delete),

    path("tuning/list/", views.tuning_list),
    path("tuning/add/", views.tuning_add),
    path("tuning/<int:nid>/edit/", views.tuning_edit),
    path("tuning/multi/", views.tuning_multi),
    path("tuning/delete/", views.tuning_delete),

    path("map/test/", views.map_test),
    path("map/download/", views.map_download),

    path("tuning/check/", views.tuning_check),
    path("tuning/<int:nid>/book/", views.tuning_book),
    path("cpa/new/", views.cpa_new),


    path("select/user/", views.select_user),
    path("select/<int:nid>/address/", views.select_address),
    path("select/<int:uid>/<int:aid>/piano/", views.select_piano),
    path("select/<int:uid>/<int:aid>/<int:pid>/cpa/", views.select_cpa),
    path("select/<int:cid>/check/", views.select_check),

    path("dataviz/", dataviz_views.index,name="map"),

    # data visualisation - yongbin test
    path("chart/list/", views.chart_list),
    path("chart/bar/", views.chart_bar),

    # path('admin/', admin.site.urls),
    # path('', DashbordView, name='dashboard'),
    path('search/', SearchFilterView, name='search'),
    path('dashboard/', DashbordView, name='dashboard'),
    # path('map/',MapView, name='map'),
    path('api/models/', models_api, name='models_api'),
    path('export-csv/', export_csv, name='export_csv'),

]
