from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.mainViewLogger, name="LogMain"),
    url('^search$', views.search_in_archives, name="search_in_archives"),
]
