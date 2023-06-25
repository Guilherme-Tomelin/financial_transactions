from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import os
import re
from io import StringIO
import csv
from .models import Transacao, Importacoes
from datetime import datetime

#views.py serve para trabalhar a lógica por trás das rotas

def index(request):
    importacoes = Importacoes.objects.all()

    return render(request, 'galeria/index.html', {'importacoes': importacoes})

def importar_arquivo(request):
        arquivo = request.FILES['file']
        nome_arquivo = arquivo.name
        extensao_arquivo = os.path.splitext(nome_arquivo)[1].lower()

        if extensao_arquivo != '.csv':
            return HttpResponse("Erro: O arquivo importado tem um formato inválido. O arquivo deve ser do tipo CSV.")

        tamanho_arquivo = arquivo.size / (1024 * 1024)
        print(f"Arquivo importado: {nome_arquivo}")
        print(f"Tamanho do arquivo: {tamanho_arquivo} MB")

        conteudo_arquivo = arquivo.read().decode('utf-8')
        arquivo_csv = StringIO(conteudo_arquivo)

        primeira_linha = next(csv.reader(arquivo_csv), None) #Se o arquivo CSV estiver vazio, ou seja, não contiver nenhuma linha, a saída será None.
        if arquivo_vazio(primeira_linha):
            arquivo_csv.close()
            return HttpResponse("Erro: O arquivo está vazio.")

        linhas_validas, linhas_invalidas = valida_linhas(arquivo_csv, primeira_linha)

        print("-------Linhas Validas-------")
        for i, linha in enumerate(linhas_validas):
            print(f"{i} - {linha}")

        print("-------Linhas Invalidas-------")
        for i, linha in enumerate(linhas_invalidas):
            print(f"{i} - {linha}")

        arquivo_csv.close()

        salvar_transacoes(linhas_validas)
        salvar_importacoes(primeira_linha)

        importacoes = Importacoes.objects.all()
        return render(request, 'galeria/index.html', {'importacoes': importacoes})

def arquivo_vazio(primeira_linha):

    """
    Verifica se o arquivo CSV está vazio.

    Utiliza a primeira linha do csv e verifica se seu conteúdo é "None"


    Args:
        primeira_linha (list): A primeira linha do arquivo CSV.

    Returns:
        bool: True se o arquivo CSV estiver vazio, False caso contrário.
    """

    if primeira_linha is None:
        return True
    else:
        return False

def valida_linhas(arquivo_csv, primeira_linha):

    """
    Realiza a validação das linhas de um arquivo CSV.

    Verifica se existem datas diferentes das demais linhas,
    identifica e ignora linhas duplicadas e verifica se há
    campos faltando.

    Args:
        arquivo_csv (io.StringIO): O objeto de arquivo CSV.
        primeira_linha (list): A primeira linha do arquivo CSV.

    Returns:
        tuple: Uma tupla contendo a lista de linhas válidas e a
        lista de linhas inválidas.
    """

    linhas_validas = []
    linhas_invalidas = []

    linhas_validas.append(primeira_linha)
    primeira_data = retorna_data(primeira_linha)
    padrao_data = re.compile(r"[0-9]{4}[-][0-9]{2}[-][0-9]{2}")
    for linha in csv.reader(arquivo_csv):
        if not datas_distintas(linha, primeira_data, padrao_data):
            linhas_invalidas.append(linha)
        elif linhas_duplicadas(linha, linhas_validas):
            continue
        elif falta_informacao(linha):
            linhas_invalidas.append(linha)
        else:
            linhas_validas.append(linha)
            print("Linha válida adicionada")
    return linhas_validas, linhas_invalidas

def retorna_data(linha):

    """
    Recebe a primeira linha do CSV, utiliza regex para encontrar a primeira data presente.


    Args:
        linha (list): Uma linha do arquivo CSV.
    Returns:
        str: Uma string formatada com o conteúdo da primeira data, excluindo o horário.
        
    """

    primeira_data = linha[-1]
    padrao_data = re.compile(r"[0-9]{4}[-][0-9]{2}[-][0-9]{2}")
    busca_data = padrao_data.search(primeira_data)

    if busca_data is None:
        raise ValueError("Data não encontrada no formato esperado")

    primeira_data_formatada = busca_data.group()
    return primeira_data_formatada

def datas_distintas(linha, primeira_data, padrao_data):

    """
    Recebe a primeira linha do CSV, utiliza regex para encontrar a primeira data presente.

    Args:
        linha (list): Uma linha do arquivo CSV.
        primeira_data: primeira data encontrada no csv através da função retorna_data
        padrao_data: o padrão criado através de regex "[0-9]{4}[-][0-9]{2}[-][0-9]{2}"
    Returns:
        bool: Retorna True caso a data seja válida e False caso contrário
        
    """

    busca_data = padrao_data.search(linha[-1])

    if busca_data and busca_data.group() == primeira_data:
        return True
    else:
        print("Linha inválida encontrada: A data não corresponde com as demais.")
        print(f"Linha: << {linha} >>")
        return False

def linhas_duplicadas(linha, linhas_validas):

    """
    Verifica se existem linhas duplicadas no arquivo CSV.

    Percorre a lista de linhas validas e verifica se a linha atual já está contida na lista.

    Args:
        linha (list): Uma linha do arquivo CSV.
        linhas_validas: lita de linhas validas
    Returns:
        bool: Retorna True caso uma linha duplicada seja encontrada e False caso contrário.
    """

    for linha_valida in linhas_validas:
        if linha == linha_valida:
            print("Linha duplicada encontrada: Duplicata ignorada.")
            print(f"Linha: << {linha} >>")
            return True
    return False

def falta_informacao(linha):

    """
    Verifica se há alguma informação faltando na linha do arquivo CSV.

    Percorre a lista de campos da linha e verifica se algum campo está vazio ou contém uma string vazia.

    Args:
        linha (list): Uma linha do arquivo CSV.

    Returns:
        bool: True se houver alguma informação faltando na linha, False caso contrário.
    """

    if any(not campo for campo in linha):
        print("Linha inválida encontrada: A linha tem um ou mais dados faltando.")
        print(f"Linha: << {linha} >>")
        return True
    return False

#--------------------------Banco--------------------------

def salvar_transacoes(linhas_validas):
    for linha in linhas_validas:
        nova_linha = Transacao(
            banco_origem=linha[0],
            agencia_origem=linha[1],
            conta_origem=linha[2],
            banco_destino=linha[3],
            agencia_destino=linha[4],
            conta_destino=linha[5],
            valor_da_transação=linha[6],
            data_e_hora_da_transacao=linha[7]
        )
        nova_linha.save()
    print("Linhas válidas adicionadas à tabela de transações.")

def salvar_importacoes(primeira_linha):

    primeira_data = retorna_data(primeira_linha)

    #Data e hora atual do sistema
    data_transacoes = datetime.strptime(primeira_data, "%Y-%m-%d").date()
    data_importacao = datetime.now()

    nova_importacao = Importacoes(
        data_transacoes = data_transacoes,
        data_importacao = data_importacao
    )
    nova_importacao.save()
    print("Nova importação adicionada à tabela de importações")