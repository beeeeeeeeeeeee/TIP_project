from django.urls import path

from . import views

app_name = 'suburb_finder'
urlpatterns = [
    path('', views.index, name="suburb_finder"),
    path('<int:suburb_id>/', views.detail, name='detail'),
    path('dashboard/', views.DashbordView, name='dashboard'),
]