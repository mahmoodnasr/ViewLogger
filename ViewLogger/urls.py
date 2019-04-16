from . import views
from django.conf.urls import include, url


urlpatterns = [
    url('^$', views.mainViewLogger, name="LogMain"),
    url('^search$', views.search_in_archives, name="search_in_archives"),
]