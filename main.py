
from corretora_app.models.cliente import Cliente
from corretora_app.models.conta_investimento import ContaInvestimento
from corretora_app.models.ativo import Ativo
from corretora_app.models.conta import Conta 
from corretora_app.database import (
    adicionar_cliente,
    salvar_conta,
    buscar_cliente_por_cpf, 
    buscar_ativo_por_ticker,
    buscar_conta_por_numero,
    buscar_carteira,
    #atualizar_buscar_carteira,
    atualizar_preco_ativo,
    atualizar_saldo_conta,
    atualizar_posicao_carteira
)
from mysql.connector import errorcode
import mysql.connector

NUMERO_LOGIN = "12345--"
def main():
    try:
        print(f"\n Carregando dados da conta {NUMERO_LOGIN}")
        conta = buscar_conta_por_numero(NUMERO_LOGIN)
        if not conta:
            print (f"erro ao tentar carregar: {NUMERO_LOGIN}")
            print ("DEV: Execute os testes novamente para descobrir a origem da falha")
        
        print (f"Cliente carregado: {conta.cliente.nome_cliente}")
        
        print("\n Carregando carteira...")
        carteira_bd = buscar_carteira(conta.id)
        conta.carteira = carteira_bd
        print ("Login bem-sucedido!")
        
        ativo = "ITUB4"
        ativo_busca = buscar_ativo_por_ticker(ativo)
        if not ativo_busca:
            print(f"Ativo de exemplo: {ativo} não encontrado")
            # programa continua porém compra/venda pode falhar
        
        print (f"\n -- Resumo da conta --")
        conta.exibir_resumo()
        
    except Exception as e:
        print(f"Erro durante a inicialização: {e}")
        return
    
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Ver Resumo da Conta")
        print("2. Depositar")
        print("3. Sacar")
        print("4. Comprar Ativo")
        print("5. Vender Ativo")
        print("6. Ver Preço do Ativo Exemplo")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n--- Resumo da Conta ---")
            conta.exibir_resumo() 
            
        elif opcao == '2':
            try:
                valor_str = input("Digite o valor a ser depositado: R$ ")
                valor_float = float(valor_str)
                conta.depositar(valor_float) 
                atualizar_saldo_conta(conta.numero_conta, conta.saldo_da_conta) 
                
                print("Depósito realizado e salvo no banco.")
                
            except (ValueError, TypeError) as e:
                print(f"Erro ao depositar: {e}")

        elif opcao == '3':
            try:
                valor_str = input("Digite o valor a ser sacado: R$ ")
                valor_float = float(valor_str)
                
                conta.sacar(valor_float)
                
                atualizar_saldo_conta(conta.numero_conta, conta.saldo_da_conta)
                
                print("Saque realizado e salvo no banco.")
                
            except (ValueError, TypeError) as e:
                print(f"Erro ao sacar: {e}")
            
        elif opcao == '4': 
            print("\n--- Comprar Ativo ---")
            try:
                print("Ativo disponível:")
                print(ativo_busca)
                print(f"Saldo Disponível: R$ {conta.saldo_da_conta:.2f}")
                
                decisao = input("Deseja comprar este ativo? (S/N): ").upper().strip()
                if decisao == 'S':
                    quantidade_str = input(f"Quantos ativos {ativo_busca.ticker} deseja comprar? ")
                    quantidade_int = int(quantidade_str)
                    conta.comprar_ativo(ativo_busca, quantidade_int)
                    
                    atualizar_saldo_conta(conta.numero_conta, conta.saldo_da_conta)
                    nova_quantidade_total = conta.carteira[ativo_busca.ticker]
                
                    atualizar_posicao_carteira(
                        conta_id=conta.id, 
                        ativo_id=ativo_busca.id, 
                        nova_quantidade=nova_quantidade_total
                    )
                    print("Compra realizada e salva no banco de dados.")
                else:
                    print("Compra cancelada.")
            except (ValueError, TypeError) as e:
                print(f"Erro ao comprar: {e}")
            
        elif opcao == '5':
            print("\n--- Vender Ativo ---")
            try:
                print("Ativos que constam na sua carteira:")
                print(conta.carteira) 
                decisao = input(f"Deseja vender {ativo_busca.ticker}? (S/N): ").upper().strip()
                
                if decisao == 'S':
                    quantidade_str = input(f"Quantos ativos {ativo_busca.ticker} deseja vender? ")
                    quantidade_int = int(quantidade_str)
                    
                    conta.vender_ativo(ativo_busca, quantidade_int)

                    atualizar_saldo_conta(conta.numero_conta, conta.saldo_da_conta)                
                    if ativo_busca.ticker in conta.carteira:
                        nova_quantidade_total = conta.carteira[ativo_busca.ticker]
                    else:
                        nova_quantidade_total = 0 
                
                    atualizar_posicao_carteira(
                        conta_id=conta.id, 
                        ativo_id=ativo_busca.id, 
                        nova_quantidade=nova_quantidade_total)
                    print("Venda realizada e salva no banco de dados.")
                else:
                    print("Venda cancelada.")
            except (ValueError, TypeError) as e:
                print(f"Erro ao vender: {e}")
            
        elif opcao == '6':
            print(f"\n--- Info Ativo Exemplo ---")
            print(ativo_busca)

        elif opcao == '7':
            print("Saindo da aplicação...")
            break 

        else:
            print("Opção inválida. Tente novamente.")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()