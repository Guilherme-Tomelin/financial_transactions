from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import os
from io import StringIO
import csv


"""
O arquivo controller.py é um módulo que contém a definição da classe 
Controller e métodos relacionados que representam a lógica de controle 
da sua aplicação. Ele é usado para organizar e centralizar a lógica de 
negócios do seu aplicativo Django.
"""

"""
Arquivo CSV é composto por:
Banco origem
Agência origem
Conta origem
Banco destino
Agência destino
Conta destino
Valor da transação
Data e hora da transação
"""

class Controller:
    def importar_arquivo(request):
        arquivo = request.FILES['file']
        nome_arquivo = arquivo.name
        tamanho_arquivo = arquivo.size / (1024 * 1024)  # arquivo.size retorna tamanho em bytes e calcula convertendo para megabytes
        print(f"Arquivo importado: {nome_arquivo}")
        print(f"Tamanho do arquivo: {tamanho_arquivo} MB")

        conteudo_arquivo = arquivo.read().decode('utf-8')  # Lê o conteúdo do arquivo em memória como uma sequência de bytes e decodifica para UTF-8
        arquivo_csv = StringIO(conteudo_arquivo)  # Cria um objeto 'StringIO' para manipular o conteúdo do arquivo como um arquivo CSV

        leitor_csv = csv.reader(arquivo_csv)
        primeira_linha = next(leitor_csv)
        primeira_data = primeira_linha[-1]
        for linha in leitor_csv:
            print(primeira_data)

        return HttpResponse()
