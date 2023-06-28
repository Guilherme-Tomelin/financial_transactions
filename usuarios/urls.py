from django.urls import path 
from usuarios.views import login, cadastro, logout

#path('caminho/', funcao, name='nome_da_rota')

urlpatterns = [
    path('login', login, name='login'),
    path('cadastro',cadastro,name='cadastro'),
    path('logout', logout, name='logout')
]