continuar = 's'

import os
arq_produtos = 'produtos_adm.txt'
 
#FUNÇÕES
def menu():
    print("\n=== Menu Principal ===\n")
    print ("Escolha uma das opções abaixo:\n1 - Adm\n2 - Op\n3 - Sair\n")
    opc = input("Informe a opção desejada:\n")
    while(opc == "" or(opc != "1" and opc != "2" and opc != "3")):
        print("Informe uma opção válida.")
        opc = input ("Informe opção desejada:")
    return opc
 
def menu_adm():
    print ("\n=== Menu Adm ===\n1 - Cadastrar novo produto\n2 - Listar produtos cadastrados\n3 - Buscar produto.\n4 - Alterar produtos cadastrados.\n5 - Remover produto\n0 - Voltar ao menu\n")
    op = input("Informe uma opção:\n")
    while(op == "" or (op != "1" and op != "2" and op != "3" and op != "4" and op != "5" and op != "0")):
        print("Informe uma opção válida")
        op = input("Informe uma opção:\n")
    return op

def Cadastrar():
    repetir = True
    while repetir:
        repetir = False  

        print("Você escolheu cadastrar novo produto.\nInsira as informações abaixo para cadastrar o novo produto.\n")
        if not os.path.exists('produtos_adm.txt'):
            open('produtos_adm.txt', 'a', encoding='utf-8').close()

        codigo_produto = input('Digite o código do produto: ').strip()
        while not (codigo_produto.isdigit() and int(codigo_produto) >= 100):
            print("Código inválido. Deve ser um número inteiro maior ou igual a 100.")
            codigo_produto = input('Digite o código do produto (número >= 100): ').strip()

        nome_produto = input('Digite o nome do produto: ').strip()
        while nome_produto == "":
            print("Insira um nome válido.")
            nome_produto = input('Digite o nome do produto: ').strip()

        preco_produto = input('Digite o valor do produto: ').strip().replace(',', '.')
        while not preco_produto.replace('.', '', 1).isdigit():
            print("Insira um valor válido. Use apenas números, ex: 12.50")
            preco_produto = input('Digite o valor do produto: ').strip().replace(',', '.')
        preco_float = float(preco_produto)

        produtos = []
        with open('produtos_adm.txt', 'r', encoding='utf-8') as arq:
            linhas = arq.readlines()
            for linha in linhas:
                partes = linha.strip().split(';')
                if len(partes) == 3:
                    codigo, nome, preco = partes
                    produtos.append([codigo, nome, preco])

        for produto in produtos:
            if produto[0] == codigo_produto:
                print(f"Código {codigo_produto} já existe. Tente outro.\n")
                repetir = True  
                break  

        if repetir:
            continue  

        produtos.append([codigo_produto, nome_produto, f"{preco_float:.2f}"])
        produtos.sort(key=lambda x: int(x[0]))

        with open('produtos_adm.txt', 'w', encoding='utf-8') as arq:
            for produto in produtos:
                arq.write(f"{produto[0]};{produto[1]};{produto[2]}\n")

        print("Produto cadastrado com sucesso!")

def listarproduto():
    print('Você escolheu Listar produtos cadastrados.\n\n=== Produtos cadastrados ===')
    lista_p = carregar_produtos()

    if not lista_p:
        print('\nNão há produtos cadastrados.')
    else:
        print("\nCódigo - Descrição - Valor unitário")
        for produto in lista_p:
            preco = produto[2].replace(',', '.')
            print(f"{produto[0]} - {produto[1]} - R${float(preco):.2f}")
    
    return lista_p

def buscarproduto():
    lista_p = carregar_produtos()

    if not lista_p:
        print("Arquivo de produtos não encontrado ou vazio.")
        return

    print('Você escolheu buscar produto.')
    codigo_busca = input("Digite o código do produto que deseja buscar: ").strip()

    for produto in lista_p:
        if produto[0].strip().lower() == codigo_busca.lower():
            print('\nProduto encontrado:')
            print(f'Código do produto: {produto[0]}')
            print(f'Nome do produto: {produto[1]}')
            print(f'Preço do produto: R${produto[2]}')
            return

    print('Produto não encontrado.')

def carregar_produtos():
    produtos = []
    if os.path.exists(arq_produtos):
        with open(arq_produtos, 'r', encoding='utf-8') as arq:
            for linha in arq:
                partes = linha.strip().split(';')
                if len(partes) == 3:
                    produtos.append(partes)
    return produtos

def alterar_cod():
    lista_p = carregar_produtos()
    print("Você escolheu alterar produto.\n")

    if not lista_p:
        print("\nNenhum produto disponível para alteração.")
        return

    print("=== Produtos cadastrados ===")
    print("Código - Descrição - Valor unitário")
    for produto in lista_p:
        print(f"{produto[0]} - {produto[1]} - R${produto[2]}")

    codigos_disponiveis = [produto[0] for produto in lista_p]

    op_alterar = input('\nDigite o código do produto que deseja alterar: ').strip()
    while op_alterar not in codigos_disponiveis:
        op_alterar = input('Código inválido. Digite um código válido: ').strip()

    indice = codigos_disponiveis.index(op_alterar)

    print(f"\nDescrição atual: {lista_p[indice][1]}")
    nova_desc = input("Digite a nova descrição do produto: ").strip()
    while nova_desc == "":
        nova_desc = input("Descrição inválida. Digite novamente: ").strip()

    print(f"\nValor atual: {lista_p[indice][2]}")
    novo_valor = input("Digite o novo valor do produto: ").strip().replace(',', '.')

    while not novo_valor.replace('.', '', 1).isdigit():
        novo_valor = input("Valor inválido. Digite um valor numérico (ex: 12.50): ").strip().replace(',', '.')

    lista_p[indice][1] = nova_desc
    lista_p[indice][2] = f"{float(novo_valor):.2f}"

    with open(arq_produtos, 'w', encoding='utf-8') as arq:
        for produto in lista_p:
            arq.write(f"{produto[0]};{produto[1]};{produto[2]}\n")

    print("\nProduto alterado com sucesso!")

def excluir_produto():
    lista_p = carregar_produtos()

    if not lista_p:
        print("\nNenhum produto disponível para exclusão.")
        return

    print("\n=== Produtos cadastrados ===")
    print("Código - Descrição - Valor unitário")
    for produto in lista_p:
        print(f"{produto[0]} - {produto[1]} - R${produto[2]}")

    codigos_disponiveis = [produto[0] for produto in lista_p]

    op_excluir = input('\nDigite o código do produto que deseja excluir: ').strip()
    while op_excluir not in codigos_disponiveis:
        op_excluir = input('Código inválido. Digite um código válido: ').strip()

    indice = codigos_disponiveis.index(op_excluir)

    print(f"\nProduto selecionado para exclusão:")
    print(f"Código: {lista_p[indice][0]}")
    print(f"Descrição: {lista_p[indice][1]}")
    print(f"Valor: R${lista_p[indice][2]}")

    confirmacao = input("\nTem certeza que deseja excluir este produto? (s para sim / n para cancelar): ").strip().lower()

    if confirmacao == 's':
        lista_p.pop(indice)

        with open(arq_produtos, 'w', encoding='utf-8') as arq:
            for produto in lista_p:
                arq.write(f"{produto[0]};{produto[1]};{produto[2]}\n")

        print("\nProduto excluído com sucesso!")
    else:
        print("\nExclusão cancelada.")

def operador():
    print('\nOlá, seja bem-vindo ao menu operador.')
    print('Escolha uma das opções abaixo:\n1 - Ver cardápio.\n2 - Fazer pedido.\n3 - Voltar ao menu.\n ')
    operador = input('Informe uma opção:\n')
    while (operador == "" or (operador != '1' and operador != '2' and operador != '3')):
        print('Informe uma opção válida.')
        operador = input('Informe uma opção:')
    return operador

def ver_cardapio():
    print('=== Cardápio ===')
    lista_p = carregar_produtos()

    if not lista_p:
        print('\nNão há produtos cadastrados')
    else:
        print("Código | Produto                | Preço")
        print("------------------------------------------")
        for produto in lista_p:
            preco = produto[2].replace(',', '.')
            print(f"{produto[0]:<6} | {produto[1]:<22} | R$ {float(preco):6.2f}")

    return lista_p

def pedido():
    import os

    arq_produtos = 'produtos_adm.txt'

    if not os.path.exists(arq_produtos):
        print("Arquivo de produtos não encontrado. Não é possível fazer pedidos.")
        return

    produtos = []
    with open(arq_produtos, 'r', encoding='utf-8') as arq:
        for linha in arq:
            partes = linha.strip().split(';')
            if len(partes) == 3:
                codigo, nome, preco = partes
                produtos.append({'codigo': codigo, 'nome': nome, 'preco': float(preco)})
    if not produtos:
        print("Não há produtos cadastrados para pedido.")
        return

    print("\n=== Cardápio ===")
    print("Código | Produto                | Preço")
    print("------------------------------------------")
    for p in produtos:
        print(f"{p['codigo']:6} | {p['nome'][:22]:22} | R$ {p['preco']:6.2f}")

    pedido_itens = []
    continuar = True 
    nome_cliente = input ("\nDigite seu nome: ") 
    while continuar:
        cod = input("Digite o código do produto para pedir (ou 0 para finalizar): ").strip()
        if cod == '0':
            continuar = False
        else:
            produto_encontrado = None
            for p in produtos:
                if p['codigo'] == cod:
                    produto_encontrado = p
                    break

            if produto_encontrado is None:
                print("Código inválido ou produto não encontrado. Tente novamente.")
            else:
                qtd_valida = False
                while not qtd_valida:
                    qtd = input(f"Quantidade de '{produto_encontrado['nome']}' que deseja pedir? ").strip()
                    if qtd.isdigit() and int(qtd) > 0:
                        qtd = int(qtd)
                        qtd_valida = True
                    else:
                        print("Informe uma quantidade válida (número inteiro maior que zero).")
                item_existe = False
                for item in pedido_itens:
                    if item['codigo'] == cod:
                        item['quantidade'] += qtd
                        item_existe = True
                        break
                if not item_existe:
                    pedido_itens.append({'codigo': cod, 'nome': produto_encontrado['nome'], 'preco': produto_encontrado['preco'], 'quantidade': qtd})

                print(f"Produto '{produto_encontrado['nome']}' adicionado ao pedido.")

    if not pedido_itens:
        print("\nNenhum produto foi pedido.")
        return

    print("\n=== Resumo do Pedido ===")
    print(f"\nNome do cliente:{nome_cliente}\n")
    total = 0
    print("Código       | Produto                | Quantidade | Preço Unitário     | Subtotal")
    print("-------------------------------------------------------------------------------------")
    for item in pedido_itens:
        subtotal = item['quantidade'] * item['preco']
        total += subtotal
        print(f"{item['codigo']:12} | {item['nome'][:21]:22} | {item['quantidade']:10} | R$ {item['preco']:15.2f} | R$ {subtotal:8.2f}")
    print("--------------------------------------------------------------------------------------")
    print(f"Total a pagar: R$ {total:.2f}\n")

#MAIN
opcao = menu()
while opcao != '3':
    if opcao == '1':
        opcao_adm = menu_adm()
        while opcao_adm != '0':
            if opcao_adm == '1':
                Cadastrar()
            elif opcao_adm == '2':
                listarproduto()
            elif opcao_adm == '3':
                buscarproduto()
            elif opcao_adm == '4':
                alterar_cod()
            elif opcao_adm == '5':
                excluir_produto()
            else:
                print("Opção inválida.")
            opcao_adm = menu_adm()
    elif opcao == '2':
        opcao_ope = operador()
        while opcao_ope != '3':
            if opcao_ope == '1':
                ver_cardapio()
            elif opcao_ope == '2':
                pedido()
            opcao_ope = operador()
    else:
        print("Opção inválida.")
    opcao = menu()
 
print("Programa encerrado.")