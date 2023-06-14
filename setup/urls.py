from django.contrib import admin
from django.urls import path, include

#utilizando include para o isolamente de urls
#include(nomeApp.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('galeria.urls')),
]
