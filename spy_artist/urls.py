from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('output', views.output, name='output'),
    path('download_artist', views.download_artist, name='download_artist'),
    path('download_info', views.download_info, name='download_info')
]