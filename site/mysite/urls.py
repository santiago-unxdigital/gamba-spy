from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('spy_artist/', include('spy_artist.urls')),
    path('admin/', admin.site.urls),
]