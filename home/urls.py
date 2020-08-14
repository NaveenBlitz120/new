from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.homefun, name='home'),
    path('map',views.map, name='map'),
]
