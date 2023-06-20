from django.shortcuts import render

#views.py serve para trabalhar a lógica por trás das rotas

def index(request):

    return render(request,'galeria/index.html')