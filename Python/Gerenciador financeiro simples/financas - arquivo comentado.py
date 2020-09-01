"""
    Título: Gerenciador financeiro simples com python
    Autor: André Vicente
        isquicha@gmail.com
        linkedin.com/in/isquicha
    Data: 29 de Julho de 2020
    Descrição: 
        Gerenciador financeiro simples, voltado a trabalhar fundamentos de lógica de programação e manipulação de arquivos com a linguagem python.
        Vídeo explicativo:

        Este arquivo faz parte de uma aula bônus para os curso de:
            Lógica de Programação e Algoritmos com Python
                https://www.udemy.com/course/programarcompython/?referralCode=2657DAE91BF990DE780E

        O programa cria um pequeno gerenciador de finanças via linha de comando, onde é possível adicionar transações a uma carteira, editar e deletar essas transações, checar o saldo, listar as transações e salvar toda a carteira em um arquivo .json. Cada transação possui um código único (identificador). O último id atribuido a uma transação sempre fica salvo na chave 'idtransacao' no arquivo .json.
    
    Observações:
        1 - Normalmente não se comenta muito o código. Ele deve, na medida do possível, ser auto explicativo. Entretanto, como se trata de um código feito para uma aula extra de um curso para iniciantes, resolvi deixá-lo rico de comentários.
        2 - Não foram levados em consideração vários aspectos que dizem respeito à performance, ao tratamento de erros e garantia de estabilidade, bem como a segurança ou escalabilidade. Este é um projeto para iniciantes =D
"""

# Começamos importando as bibliotecas auxiliares
# datetime para podermos pegar o valor de data e hora atuais
# json para podermos exportar (e posteriormente importar) a carteira com todas as transações
from datetime import datetime
import json

# Primeiramente tentamos abrir o arquivo da carteira e pegar seu conteúdo
try:
    # Abrimos o arquivo carteira.json (que estará na mesma pasta deste arquivo financas.py)
    with open("carteira.json", "r") as arquivo:
        # E lemos o conteúdo do arquivo com json.loads, visto que salvaremos os valores no formato json
        # O valor lido é então enviado à variável global 'carteira', cujo tipo é um dicionário python
        carteira = json.loads(arquivo.read())

    # Já em posse da carteira, atribuimos à variável global 'id_transacao'
    # o valor do próximo id a ser utilizado na criação de uma nova transação
    id_transacao = carteira["idtransacao"]
    # Em seguida descartamos essa chave do dicionário (para evitar problemas na listagem)
    carteira.pop("idtransacao")

# Se ocorrer algum erro dentro do bloco try, com ressalva aos dois esperados:
# 1 - O arquivo carteira.json ainda não existir
# 2 - A chave 'idtransacao' não existir dentro do arquivo .json
# Tudo feito no bloco try é descartado, e executa-se o bloco except
except:
    # Criamos uma carteira vazia
    carteira = {}
    # E inicializamos o id_transacao em 1,
    # já que iremos colocar a primeira transação do programa
    id_transacao = 1

# Daqui para baixo até antes do laço while são criadas as funções que serão responsáveis
# por cada uma das funcionalidades do programa. Os nomes são auto explicativos.


def listarTransacoes():
    # Se a carteira estiver vazia, printa que não há transações
    if len(carteira) == 0:
        print("\nSem transações!")
        return  # Encerra a função sem executar o resto dela

    # Se tem alguma transação na carteira, o resto abaixo é executado
    print("\nSuas transações: ")

    # Para cada transação ordenada de forma decrescente pelo id da mesma
    for transacao in sorted(
        carteira.values(),
        key=lambda transacao: str(transacao["identificador"]),
        reverse=True,
    ):
        # Printa a transação
        # Note que este print está dentro do laço for
        print(
            f'{transacao["identificador"]} - {transacao["data"]} - {transacao["descricao"]}: R${transacao["valor"]:.2f}'
        )


def adicionarTransacao():
    # Sobre a linha 'global id_transacao'
    # Quando queremos ler o valor de uma variável global dentro
    # de uma função, podemos simplesmente usar o nome dela
    # Entretanto, se quisermos mudar o valor da mesma, precisamos especificar
    # que estamos usando a variável global com a linha abaixo
    # Isto acontece pois se não fizéssemos isso, existiriam duas variáveis
    # com o mesmo nome, uma que é global e outra que só existe dentro dessa função
    # A prática de usar variáveis globais assim é desencorajada, e não é uma
    # boa prática de programação, mas fiz assim para mostrar a possibilidade,
    # bem como para não adicionar uma camada de complexidade à aula
    # A melhor maneira seria passar essa variável global como parâmetro para
    # a função, alterar localmente e em seguida retornar esse valor
    # e utilizar o retorno para ajustar a variável global.

    global id_transacao

    # Pegamos os dados da transação
    descricao = input("\nDigite a descrição da transação: ")
    # Lembrando que o delimitador de decimais é o . e não a ,
    valor = float(
        input("Digite o valor da transação (com sinal de - se for despesa): ")
    )
    data = str(datetime.now())

    # Criamos um dicionário para empacotar os dados dessa transação
    transacao = {
        "valor": valor,
        "descricao": descricao,
        "data": data,
        "identificador": str(id_transacao),
    }

    # Adicionamos a transação na carteira, na chave id_numerodoid
    # no caso, numerodoid é o número do id da transação
    # Exemplo, se id_transacao = 5, vamos adicionar na carteira
    # na chave id_5 o valor transacao (o dicionário)
    carteira["id_" + str(id_transacao)] = transacao

    # Fazemos o update do id para a próxima transação que for
    # adicionada ter um id maior
    id_transacao += 1
    print("Transação adicionada com sucesso!")


def deletarTransacao():
    # Já adicionamos o id_ antes do numero da transação a deletar
    # se o usuário digitar, por exemplo, 5
    # identificador vai ser id_5
    identificador = "id_" + input("\nDigite o id da transação que quer deletar: ")

    # Tiramos a transação da carteira com o pop
    # Como o pop além de tirar da carteira retorna o valor tirado,
    # colocamos esse valor na variável local transacao para podermos
    # informar ao usuário qual foi a transação removida
    transacao = carteira.pop(identificador)
    print(
        f'Transação {transacao["identificador"]} - "{transacao["descricao"]}", no valor de R${transacao["valor"]:.2f} foi excluída!'
    )


def editarTransacao():
    # Como vamos precisar do número da transação para colocar na lista de id
    # o passo a passo é separado se comparado a função anterior
    id_transacao = int(input("\nDigite o id da transação que quer editar: "))
    identificador = "id_" + str(id_transacao)

    descricao = input("Digite a nova descrição da transação: ")
    valor = float(input("Digite o novo valor da transação: "))
    mudar_data = input(
        "Digite S para mudar a data da transação para a data atual ou N para manter a data antiga: "
    ).upper()
    if mudar_data == "S":
        data = str(datetime.now())
    else:
        # Se o usuário não quiser mudar a data, mantemos a data antiga
        data = carteira[identificador]["data"]

    # O resto é igual a função de adicionar uma nova transação
    transacao = {
        "valor": valor,
        "descricao": descricao,
        "data": data,
        "identificador": id_transacao,
    }

    carteira["id_" + str(id_transacao)] = transacao

    print(f"Transação {id_transacao} editada com sucesso!")


def consultarSaldo():
    saldo = 0
    for transacao in carteira.values():
        # Adicionamos o valor de cada transação ao saldo
        saldo += transacao["valor"]

    print(f"\nSeu saldo atual é R${saldo:.2f}")


def salvarCarteira():
    # Copiamos a carteira
    # Não podemos usar a sintaxe c = carteira (o que parece ser uma cópia)
    # pois as variáveis carteira e c estariam referenciando a mesma carteira
    # na memória RAM, e teríamos problemas depois de inserir idtransacao
    c = carteira.copy()
    # Adicionamos a variável idtransacao à carteira
    c["idtransacao"] = id_transacao

    # Abrimos o arquivo json
    with open("carteira.json", "w") as arquivo:
        # Escrevemos a carteira no arquivo, com o formato json
        arquivo.write(json.dumps(c))


while True:
    # Salva a operação do menu na variável op, transformando tudo em maísculo
    op = input(
        """\nDigite:
        \rL - Listar transações
        \rA - Adicionar transação
        \rD - Deletar transação
        \rE - Editar transação
        \rS - Consultar saldo atual
        \rQ - Sair do programa
        \rSua entrada: """
    ).upper()

    # Testa qual foi a operação escolhida e executa as funções
    # condizentes com a mesma
    if op == "A":
        adicionarTransacao()
        salvarCarteira()
    elif op == "D":
        deletarTransacao()
        salvarCarteira()
    elif op == "E":
        editarTransacao()
        salvarCarteira()
    elif op == "L":
        listarTransacoes()
    elif op == "S":
        consultarSaldo()
    elif op == "Q":
        exit()
    else:
        # Se a pessoa digitar qualquer outra coisa, retorna que a operação
        # é inválida
        print("Operação inválida!")

