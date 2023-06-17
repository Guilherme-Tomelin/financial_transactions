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

        leitor_csv = csv.reader(arquivo_csv)

        for linha in leitor_csv:
            print("a")

        

        def arquivo_vazio(arquivo_csv):

            """
            - Retorna TRUE se o arquivo estiver vazio e FALSE se o arquiv não estiver vazio.

            - Se o arquivo que foi feito upload estiver vazio, uma mensagem de 
            erro deve ser exibida para o usuário, indicando tal situação;

            - next(leitor_csv) tenta obter a primeira linha do arquivo CSV usando a função next().
            A função next() retorna o próximo item de um iterável, no caso, o leitor_csv. Se não houver próxima 
            linha, a exceção StopIteration será lançada.
            """

            leitor_csv = csv.reader(arquivo_csv)
            primeira_linha = next(leitor_csv)

            try:
                primeira_linha = next(leitor_csv)
            except StopIteration:
                return True #Arquivo vazio
            return False #Arquivo não está vazio

        def retorna_data(arquivo_csv):

            """
            - Retorna a data da primeira linha do arquivo CSV
            - Exemplo de data 2022-01-01T07:30:00
            """


            leitor_csv = csv.reader(arquivo_csv)
            primeira_linha = next(leitor_csv)

            primeira_data = primeira_linha[-1]

            padrao = re.compile("[0-9]{4}[-][0-9]{2}[-][0-9]{2}")
            busca = padrao.search(primeira_data)

            primeira_data_formatada = busca.group(primeira_data)

            return primeira_data_formatada


        def datas_distintas(arquivo_csv):

            """
            - Retorna TRUE se a linha for válida, Retorna FALSE se for inválida (diferente da primeira)

            - Se alguma transação posterior estiver com outra data diferente, 
            ela deve ser ignorada e não ser salva no banco de dados;
            """

            #Exemplo de data 2022-01-01T07:30:00

            primeira_data = retorna_data(arquivo_csv)
            
            leitor_csv = csv.reader(arquivo_csv)
            for linha in leitor_csv:
        
                padrao = re.compile("[0-9]{4}[-][0-9]{2}[-][0-9]{2}")
                busca = padrao.search(linha)

                if busca == primeira_data:
                    continue
                elif busca != primeira_data:
                    return False
                
            return True
        

        def linhas_duplicadas(arquivo_csv):

            """
            - Retorna TRUE se não encontrar nenhuma duplicata no CSV, retorna FALSE se encontrar alguma duplicata.

            - A aplicação não deve "duplicar" transações de um determinado dia, ou seja, se o upload de transações de um determinado dia já tiver sido realizado anteriormente, uma mensagem de erro deve ser exibida ao usuário, indicando que as transações daquela data já foram realizadas;

            """

            leitor_csv = csv.reader(arquivo_csv)
            for i, linha_base in enumerate(leitor_csv):
                for j, linha in enumerate(leitor_csv, start=i+1):
                    if linha_base == linha:
                        print("Erro: As linhas não devem se repetir.")
                        print(f"Posição 1: {i}")
                        print(f"Linha 1: << {linha_base} >>")
                        print(f"Posição 2: {j}")
                        print(f"Linha 2: << {linha} >>")
                        return False
            return True





        def falta_informacao(arquivo_csv):
            """
            - Retorna TRUE se falta alguma informação, retorna FALSE se não falta nenhuma informação.
            - Todas as informações da transação são obrigatórias, ou seja, se alguma transação estiver com alguma informação faltando, ela também deve ser ignorada e nao ser salva no banco de dados.
            """
    
            padrao = re.compile(",,")

            leitor_csv = csv.reader(arquivo_csv)
            for linha in leitor_csv:
                busca = padrao.search(linha)
                if busca:
                    return True
                else:
                    continue
            return False
            
            


        


        return HttpResponse()
