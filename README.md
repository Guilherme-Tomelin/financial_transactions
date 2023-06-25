# Projeto Django: financial_transactions

[em desenvolvimento]

## Visão Geral
Este é o repositório do projeto Django "financial_transactions". O projeto tem como objetivo desenvolver uma aplicação web tradicional para realizar a análise de transações financeiras e identificar possíveis transações suspeitas. O projeto serve como uma experiência de aprendizado e para adicionar ao portfólio.

## Requisitos
- Python
- Django
- (Opcional) Projeto externo para geração de simulação de arquivo CSV: [SimuladorDadosBancarios](https://github.com/Guilherme-Tomelin/SimuladorDadosBancarios)
- Bibliotecas Python listadas no arquivo requirements.txt

## Configuração do Ambiente de Desenvolvimento
1. Clone este repositório.
2. Instale as dependências listadas no arquivo requirements.txt.
3. Execute o projeto Django localmente.

## Como Executar o Projeto Localmente
1. Navegue até o diretório raiz do projeto.
2. Execute o comando `python manage.py runserver` para iniciar o servidor de desenvolvimento.
3. Acesse o projeto no navegador usando o endereço `http://localhost:8000`.

<!-- 
## Documentação
Consulte a documentação completa para obter mais detalhes sobre a estrutura do projeto, requisitos, funcionalidades e outros aspectos importantes. [Documentação Completa](./documentation.md) -->

## Funcionalidades Principais
- Tela de Login e Senha para autenticação de usuários.
- Cadastro de usuários com diferentes permissões.
- Importação de arquivos CSV contendo transações financeiras.
- Validação e persistência das informações dos arquivos importados.
- Listagem das importações realizadas.
- Tela de Administração para consultar os bancos de dados.

## Telas Principais
- Tela Inicial: Lista as importações de arquivos CSV, exibindo a data do arquivo e a data da importação.
- Tela de Login: Permite que os usuários façam login no sistema.
- Tela de Cadastro: Permite que novos usuários se cadastrem no sistema.
- Tela de Administração: Permite consultar e gerenciar os bancos de dados.

## Arquitetura
O projeto segue a arquitetura Model-View-Template (MVT) do Django, onde os modelos representam as entidades do sistema, as views controlam a lógica de negócios e as templates são responsáveis pela apresentação dos dados.

## Modelos de Dados
- Transacao:
  - banco_origem (CharField): Nome do banco de origem da transação.
  - agencia_origem (IntegerField): Número da agência de origem da transação.
  - conta_origem (CharField): Número da conta de origem da transação.
  - banco_destino (CharField): Nome do banco de destino da transação.
  - agencia_destino (IntegerField): Número da agência de destino da transação.
  - conta_destino (CharField): Número da conta de destino da transação.
  - valor_da_transação (DecimalField): Valor da transação.
  - data_e_hora_da_transacao (DateTimeField): Data e hora da transação.

- Importacoes:
  - data_transacoes (DateField): Data das transações importadas.
  - data_importacao (DateTimeField): Data e hora da importação das transações.

## Contribuição
Contribuições são bem-vindas! Se você encontrar algum problema, tiver sugestões ou apenas quiser bater um papo sobre programação, sinta-se à vontade para entrar em contato através do [Meu Linkedin](https://www.linkedin.com/in/guilherme-tomelin-dos-santos-1b7a73199/).

