from django.urls import path #importantedo método path do django
from galeria.views import index #importando minha função index de views
from . import views

urlpatterns = [
    path('',index),
    path('importar', views.importar_arquivo, name='importar_arquivo'),
]