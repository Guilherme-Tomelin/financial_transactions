from django.db import models

"""O arquivo models.py no Django é onde você define as classes de modelo, 
que representam as tabelas do banco de dados. Simplificadamente, 
o modelo é usado para definir a estrutura e os tipos de dados dos 
objetos que serão armazenados no banco de dados.

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



class Transacao(models.Model):


    banco_origem = models.CharField(max_length=100, null = False, blank = False)
    agencia_origem = models.IntegerField(null = False, blank = False)
    conta_origem = models.CharField(max_length=7, null = False, blank = False)
    banco_destino = models.CharField(max_length=100, null = False, blank = False)
    agencia_destino = models.IntegerField(null = False, blank = False)
    conta_destino = models.CharField(max_length=7, null = False, blank = False)
    valor_da_transação = models.DecimalField(max_digits=10, decimal_places=2)
    data_e_hora_da_transacao = models.DateTimeField(null = False, blank = False)
    
    def __str__(self):
        return f"""
            Banco origem [{self.banco_origem}]
            Agência origem [{self.agencia_origem}]
            Conta origem [{self.conta_origem}]
            Banco destino [{self.banco_destino}]
            Agência destino [{self.agencia_destino}]
            Conta destino [{self.conta_destino}]
            Valor da transação [{self.valor_da_transação}]
            Data e hora da transação [{self.data_e_hora_da_transacao}]
        """

class Importacoes(models.Model):
    data_transacoes = models.DateField()
    data_importacao = models.DateTimeField()

