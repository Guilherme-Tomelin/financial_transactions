from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import os


class Controller:
    def importar_arquivo(request):
        arquivo = request.FILES['file']
        nome_arquivo = arquivo.name
        tamanho_arquivo = arquivo.size / (1024 * 1024)  # arquivo.size retorna tamanho em bytes e calcula convertendo para megabytes
        print(f"Arquivo importado: {nome_arquivo}")
        print(f"Tamanho do arquivo: {tamanho_arquivo} MB")

        return HttpResponse()
