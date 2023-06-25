from django.contrib import admin
from galeria.models import Transacao, Importacoes

"""
    Transacao{
        banco_origem
        agencia_origem 
        conta_origem 
        banco_destino 
        agencia_destino 
        conta_destino 
        valor_da_transação
        data_e_hora_da_transacao
    }
    
    Importacoes{
        data_transacoes
        data_importacao 
    
    }
"""

class ListandoTransacoes(admin.ModelAdmin):
    list_display = ("id","banco_origem","conta_origem" ,"banco_destino","conta_destino" ,"valor_da_transação" ,"data_e_hora_da_transacao")
    list_display_links = ("id","data_e_hora_da_transacao")
    search_fields = ("id",)
    list_filter = ("banco_origem",)

class ListandoImportacoes(admin.ModelAdmin):
    list_display = ("id", "data_transacoes", "data_importacao")
    list_display_links = ("id",)
    search_fields = ("id",)
    list_filter = ("data_importacao",)

admin.site.register(Transacao, ListandoTransacoes)
admin.site.register(Importacoes, ListandoImportacoes)


