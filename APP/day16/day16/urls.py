"""day16 URL Configuration

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
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

# from google import views as view

from app01 import views

urlpatterns = [
    # set media folder
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}, name="media"),

    # path("admin/", admin.site.urls),
    path("depart/list/", views.depart_list),
    path("depart/add/", views.depart_add),
    path("depart/delete/", views.depart_delete),
    # http://127.0.0.1:8000/depart/1/edit/
    path("depart/<int:nid>/edit/", views.depart_edit),
    path("depart/multi/", views.depart_multi),

    path("user/list/", views.user_list),
    path("user/add/", views.user_add),
    path("user/model/form/add/", views.user_model_form_add),
    path("user/<int:nid>/edit/", views.user_edit),
    path("user/<int:nid>/delete/", views.user_delete),

    path("pretty/list/", views.pretty_list),
    path("pretty/add/", views.pretty_add),
    path("pretty/<int:nid>/edit/", views.pretty_edit),
    path("pretty/<int:nid>/delete/", views.pretty_delete),

    path("admin/list/", views.admin_list),
    path("admin/add/", views.admin_add),
    path("admin/<int:nid>/edit/", views.admin_edit),
    path("admin/<int:nid>/delete/", views.admin_delete),
    path("admin/<int:nid>/reset/", views.admin_reset),

    path("login/", views.login),
    path("logout/", views.logout),
    path("image/code/", views.image_code),

    path("task/list/", views.task_list),
    path("task/ajax/", views.task_ajax),
    path("task/add/", views.task_add),

    path("order/list/", views.order_list),
    path("order/add/", views.order_add),
    path("order/delete/", views.order_delete),
    path("order/detail/", views.order_detail),
    path("order/edit/", views.order_edit),

    path("chart/list/", views.chart_list),
    path("chart/bar/", views.chart_bar),
    path("chart/pie/", views.chart_pie),
    path("chart/line/", views.chart_line),

    path("upload/list/", views.upload_list),
    path("upload/form/", views.upload_form),
    path("upload/model/form/", views.upload_model_form),

    path("city/list/", views.city_list),
    path("city/add/", views.city_add),

    path("map/autofill/", views.map_autofill),
    path("map/autofill2/", views.map_autofill2),

    path("address/list/", views.address_list),
    path("address/add/", views.address_add),

    path("address1/list/", views.address1_list),
    path("address1/add/", views.address1_add),
    path("address1/multi/", views.address1_multi),

    path("map/test1/", views.map_test1),

]
