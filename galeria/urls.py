from django.urls import path #importantedo método path do django
from galeria.views import index #importando minha função index de views
from galeria.Controller import Controller

urlpatterns = [
    path('',index),
    path('importar', Controller.importar_arquivo, name='importar_arquivo'),
]