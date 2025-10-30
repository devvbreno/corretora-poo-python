from corretora_app.models.cliente import Cliente
from corretora_app.models.conta_investimento import ContaInvestimento
from corretora_app.models.ativo import Ativo
from corretora_app.models.conta import Conta 
from corretora_app.database import adicionar_cliente
from corretora_app.database import buscar_cliente_por_cpf
from corretora_app.database import buscar_ativo_por_ticker
from corretora_app.database import atualizar_preco_ativo
from corretora_app.database import salvar_conta
from mysql.connector import errorcode
import mysql.connector


def main():
    print("--- Bem-vindo(a) à Corretora POO ---")

    # DADOS EM MEMÓRIA (Substitui o Banco de Dados por enquanto)
    try:
        cliente_principal = Cliente(nome_cliente="Breno", cpf_cliente="11122233344")
        conta_principal = ContaInvestimento(cliente=cliente_principal, numero_conta="12345-6")
        ativo_exemplo = Ativo(ticker="PYTH4", nome_empresa="Python Corp", preco_atual=50.0)
        print("Dados iniciais carregados.")
        print(conta_principal)
        
        # Tentativa de buscar o cliente por cpf
        print("\n Tentando buscar o cliente no banco de dados por cpf...")
        cliente_teste = buscar_cliente_por_cpf(cliente_principal.cpf_limpo)
        if cliente_teste:
            print ("Cliente Encontrado: ", cliente_teste)
        else:
            print ("Cliente não encontrado.")
        
        # Tentativa de buscar ativo por ticker
        print("\n Tentando buscar o ativo no banco de dados por ticker...")
        ativo_teste = buscar_ativo_por_ticker (ativo_exemplo.ticker)
        if ativo_teste:
            print ("Ativo Encontrado: ", ativo_teste)
        else:
            print ("Ativo não encontrado.")
        
        # Teste de Atualização de valor Válida

        ticker_teste = "PYTH4" 
        novo_preco_valido = 45.10

        try:
            print(f"\nTentando atualizar {ticker_teste} para R$ {novo_preco_valido:.2f}...")
            ativo_antes = buscar_ativo_por_ticker(ticker_teste) 
            atualizar_preco_ativo(ticker_teste, novo_preco_valido)
            ativo_depois = buscar_ativo_por_ticker(ticker_teste) 

            if ativo_depois and ativo_depois.preco_atual == novo_preco_valido:
                print(f"-> SUCESSO: Preço de {ticker_teste} atualizado de R$ {ativo_antes.preco_atual:.2f} para R$ {ativo_depois.preco_atual:.2f}.")
            elif ativo_antes:
                print(f"-> FALHA: Preço de {ticker_teste} NÃO foi atualizado corretamente (continua R$ {ativo_antes.preco_atual:.2f}).")
            else:
                print(f"-> ERRO: Ativo {ticker_teste} não encontrado para teste.")

        except Exception as e:
            print(f"ERRO INESPERADO durante atualização válida: {e}")

        # Teste de salvar cliente 
        try:
            print(f"\nTentando adicionar o cliente {cliente_principal.nome_cliente} (CPF: {cliente_principal.cpf_limpo}) ao banco de dados...")
            
            cliente_existente = buscar_cliente_por_cpf(cliente_principal.cpf_limpo)
            
            if not cliente_existente:
                adicionar_cliente(cliente_principal.nome_cliente, cliente_principal.cpf_limpo)
                print("-> SUCESSO: Cliente adicionado.")
                
                cliente_apos_add = buscar_cliente_por_cpf(cliente_principal.cpf_limpo)
                if cliente_apos_add:
                    print(f"-> VERIFICAÇÃO: Cliente {cliente_apos_add.nome_cliente} encontrado no banco.")
                else:
                    print(f"-> FALHA NA VERIFICAÇÃO: Cliente não encontrado após adição.")
            else:
                print(f"-> INFO: Cliente (CPF: {cliente_principal.cpf_limpo}) já existe no banco. Teste de adição pulado.")

        except mysql.connector.Error as db_error:
            if db_error.errno == errorcode.ER_DUP_ENTRY:
                print(f"-> AVISO: Cliente (CPF: {cliente_principal.cpf_limpo}) já existe no banco (Erro de Duplicidade).")
            else:
                print(f"-> ERRO DE BANCO DE DADOS ao salvar cliente: {db_error}")
        except Exception as e:
            print(f"-> ERRO INESPERADO ao salvar cliente: {e}")
            
        # --- Teste de salvar conta ---
        try:
            print(f"\nTentando salvar a conta {conta_principal.numero_conta} no banco...")
            
            # Precisamos do cliente com ID para salvar a conta
            cliente_com_id = buscar_cliente_por_cpf(cliente_principal.cpf_limpo)
            if not cliente_com_id:
                raise ValueError("Cliente da conta não encontrado no banco para salvar a conta.")
            
            # Garantir que a conta em memória tenha o cliente com ID
            conta_principal.cliente = cliente_com_id 

            # Verificamos se a conta já existe antes de tentar salvar
            # (Precisaríamos de uma função 'buscar_conta_por_numero' para isso,
            # por enquanto, vamos apenas tentar salvar e tratar o erro de duplicidade)

            novo_id_conta = salvar_conta(conta_principal)
            
            if novo_id_conta:
                print(f"-> SUCESSO: Conta salva no banco com ID: {novo_id_conta}")
            else:
                print("-> FALHA: salvar_conta() não retornou um ID.")

        except mysql.connector.Error as db_error:
            if db_error.errno == errorcode.ER_DUP_ENTRY:
                print(f"-> INFO: Conta (Número: {conta_principal.numero_conta}) já existe no banco.")
            else:
                print(f"-> ERRO DE BANCO DE DADOS ao salvar conta: {db_error}")
        except Exception as e:
            print(f"-> ERRO INESPERADO ao salvar conta: {e}")
        
        # --- Fim do teste ---
    except ValueError as e:
        print(f"Erro DE VALOR ao inicializar dados: {e}")
        return 
    
    except mysql.connector.Error as db_error:
        print(f"Erro DE BANCO DE DADOS ao inicializar dados: {db_error}")

    except Exception as e:
        print(f"Erro DESCONHECIDO ao inicializar dados: {e}")
        return


    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Ver Saldo e Carteira")
        print("2. Depositar")
        print("3. Sacar")
        print("4. Comprar Ativo")
        print("5. Vender Ativo")
        print("6. Ver Preço do Ativo Exemplo")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        # Lógica do Menu
        if opcao == '1':

            print("\n--- Resumo da Conta ---")
            print(conta_principal)
            print(f"Saldo Disponível: R$ {conta_principal.saldo_da_conta:.2f}")
            
        elif opcao == '2':
            try:
                valor_str = input("Digite o valor a ser depositado:")
                valor_float = float(valor_str)
                conta_principal.depositar(valor_float)
            except ValueError as e:
                return print(f"Erro ao depositar: {e}")

        elif opcao == '3':
            try:
                valor_str = input("Digite o valor a ser sacado:")
                valor_float = float(valor_str)
                conta_principal.sacar(valor_float)
            except ValueError as e:
                return print(f"Erro ao sacar: {e}")
            
        elif opcao == '4.':
            print("\n--- Comprar Ativo ---")
            try:
                print("Ativo disponivel:")
                print(ativo_exemplo)
                print(f"Saldo Disponível: R$ {conta_principal.saldo_da_conta:.2f}")
                decisao = input("Deseja comprar este ativo? (S/N)").upper().strip()
                if decisao == 'S':
                    quantidade_str = input(f"Quantos ativos {ativo_exemplo.ticker} deseja comprar?")
                    quantidade_int = int(quantidade_str)
                    conta_principal.comprar_ativo(ativo_exemplo, quantidade_int)
                else:
                    print("Compra cancelada")
            except ValueError as e:
                print(f"Erro ao comprar: {e}")
            

        elif opcao == '5':
            print("\n--- Vender Ativo ---")
            try:
                print("Ativos que constam na sua carteira:")
                print(conta_principal.carteira)
                decisao = input("Deseja vender este ativo? (S/N)").upper().strip()
                if decisao == 'S':
                    quantidade_str = input(f"Quantos ativos {ativo_exemplo.ticker} deseja vender?")
                    quantidade_int = int(quantidade_str)
                    conta_principal.vender_ativo(ativo_exemplo, quantidade_int)
                else:
                    print("Venda cancelada")
            except ValueError as e:
                print(f"Erro ao vender: {e}")
            
        elif opcao == '6':
            print(f"\n--- Info Ativo Exemplo ---")
            print(ativo_exemplo)

        elif opcao == '7':
            print("Saindo da aplicação...")
            break 

        else:
            print("Opção inválida. Tente novamente.")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()