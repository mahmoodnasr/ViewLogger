from django.urls import path as url
from . import views


urlpatterns = [
    url('', views.mainViewLogger, name="LogMain"),
    url('search/', views.search_in_archives, name="search_in_archives"),
]