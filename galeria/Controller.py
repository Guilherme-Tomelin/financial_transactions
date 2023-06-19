from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import os
import re
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
        
        linhas_validas, linhas_invalidas = valida_linhas(arquivo_csv)

        print("-------Linhas Validas-------")

        for i, linha in enumerate(linhas_validas):
            print(f"{i} - {linha}")

        print("-------Linhas Invalidas-------")


        for i, linha in enumerate(linhas_invalidas):
            print(f"{i} - {linha}")

        arquivo_csv.close()
        return HttpResponse()
    
def valida_linhas(arquivo_csv):

    """
    - Utiliza as funções booleanas para fazer todas as validações e retornar uma tupla com uma lista das linhas validas e outra com as linhas invalidas.

    - Verifica se o arquivo está vazio
    - Verifica se tem alguma data diferente das demais
    - Verifica se tem linhas duplicadas
    - Verifica se tem algum dado faltando
    """

    linhas_validas = []
    linhas_invalidas = []

    
    leitor_csv = csv.reader(arquivo_csv)
    primeira_linha = next(leitor_csv)

    if not arquivo_vazio(arquivo_csv):
        linhas_validas.append(primeira_linha)
        primeira_data = retorna_data(arquivo_csv)
        padrao_data = re.compile(r"[0-9]{4}[-][0-9]{2}[-][0-9]{2}")
        for linha in leitor_csv:
            if not datas_distintas(linha, primeira_data, padrao_data):
                linhas_invalidas.append(linha)
            elif linhas_duplicadas(linha, linhas_validas):
                continue
            elif falta_informacao(linha):
                linhas_invalidas.append(linha)
            else:
                linhas_validas.append(linha)
                print("Linha valida adicionada")
            
        return linhas_validas, linhas_invalidas
        

def arquivo_vazio(arquivo_csv):

    """
    - Retorna TRUE se o arquivo estiver vazio e FALSE se o arquivo não estiver vazio.

    - Se o arquivo que foi feito upload estiver vazio, uma mensagem de 
    erro deve ser exibida para o usuário, indicando tal situação;

    - next(leitor_csv) tenta obter a primeira linha do arquivo CSV usando a função next().
    A função next() retorna o próximo item de um iterável, no caso, o leitor_csv. Se não houver próxima 
    linha, a exceção StopIteration será lançada.
    """

    arquivo_csv.seek(0)
    leitor_csv = csv.reader(arquivo_csv)

    try:
        primeira_linha = next(leitor_csv)
    except StopIteration:
        print("Erro: O arquivo está vazio.")
        return True #Arquivo vazio
    print("O arquivo não está vazio")
    return False #Arquivo não está vazio

def retorna_data(arquivo_csv):

    """
    - Retorna a data da primeira linha do arquivo CSV
    - Exemplo de data 2022-01-01T07:30:00
    """

    leitor_csv = csv.reader(arquivo_csv)
    primeira_linha = next(leitor_csv)
    primeira_data = primeira_linha[-1]

    padrao_data = re.compile(r"[0-9]{4}[-][0-9]{2}[-][0-9]{2}")
    busca_data = padrao_data.search(primeira_data)

    if busca_data is None:
        raise ValueError("Data não encontrada no formato esperado")

    primeira_data_formatada = busca_data.group()
    return primeira_data_formatada


def datas_distintas(linha, primeira_data, padrao_data):

    """
    - Retorna TRUE se a linha for válida, Retorna FALSE se for inválida (diferente da primeira)

    - Se alguma transação posterior estiver com outra data diferente, 
    ela deve ser ignorada e não ser salva no banco de dados;
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
    - Retorna TRUE se não encontrar nenhuma duplicata no CSV, retorna FALSE se encontrar alguma duplicata.

    - A aplicação não deve "duplicar" transações de um determinado dia, ou seja, se o upload de transações de um determinado dia já tiver sido realizado anteriormente, uma mensagem de erro deve ser exibida ao usuário, indicando que as transações daquela data já foram realizadas;

    """

    for linha_valida in linhas_validas:
        if linha == linha_valida:
            print("Linha duplicada encontrada: Duplicata ignorada.")
            print(f"Linha: << {linha} >>")
            return True
    return False

def falta_informacao(linha):
    """
    - Retorna TRUE se falta alguma informação, retorna FALSE se não falta nenhuma informação.
    - Todas as informações da transação são obrigatórias, ou seja, se alguma transação estiver com alguma informação faltando, ela também deve ser ignorada e nao ser salva no banco de dados.
    """

    if any(not campo for campo in linha):
        print("Linha inválida encontrada: A linha tem um ou mais dados faltando.")
        print(f"Linha: << {linha} >>")
        return True
    return False

            
