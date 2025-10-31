# main.py (Versão Corrigida e Refinada)

from corretora_app.models.cliente import Cliente
from corretora_app.models.conta_investimento import ContaInvestimento
from corretora_app.models.ativo import Ativo
from corretora_app.models.conta import Conta 
# Importação completa
from corretora_app.database import (
    adicionar_cliente, 
    buscar_cliente_por_cpf, 
    buscar_ativo_por_ticker, 
    atualizar_preco_ativo, 
    salvar_conta,
    atualizar_saldo_conta,
    buscar_conta_por_numero
)
from mysql.connector import errorcode
import mysql.connector

# Importação de classes necessárias para o database.py
from corretora_app.models.conta import Conta
from corretora_app.models.cliente import Cliente
from corretora_app.models.ativo import Ativo
from corretora_app.models.conta_investimento import ContaInvestimento


def main():
    print("--- Bem-vindo(a) à Corretora POO ---")

    # --- BLOCO DE INICIALIZAÇÃO E TESTE DE BANCO ---
    try:
        # 1. Cria objetos em memória (ainda necessários para o menu)
        cliente_principal = Cliente(nome_cliente="Breno", cpf_cliente="11122233344")
        ativo_exemplo = Ativo(ticker="PYTH4", nome_empresa="Python Corp", preco_atual=50.0)
        
        # 2. Garante que o cliente de teste exista no banco
        print("\nVerificando cliente principal no banco de dados...")
        cliente_com_id = buscar_cliente_por_cpf(cliente_principal.cpf_limpo)
        if not cliente_com_id:
            print(f"Cliente (CPF: {cliente_principal.cpf_limpo}) não encontrado. Adicionando...")
            adicionar_cliente(cliente_principal.nome_cliente, cliente_principal.cpf_limpo)
            cliente_com_id = buscar_cliente_por_cpf(cliente_principal.cpf_limpo)
        
        if not cliente_com_id:
            raise ValueError("Falha crítica ao criar/buscar cliente principal.")
        print(f"Cliente (ID: {cliente_com_id.id}) carregado do banco.")
        
        # 3. Cria o objeto Conta principal USANDO o cliente com ID
        conta_principal = ContaInvestimento(cliente=cliente_com_id, numero_conta="12345-6")
        print("Objeto ContaInvestimento principal criado.")

        # 4. Garante que a conta de teste exista no banco
        print(f"\nVerificando conta {conta_principal.numero_conta} no banco...")
        conta_buscada = buscar_conta_por_numero(conta_principal.numero_conta)
        if not conta_buscada:
            print(f"Conta {conta_principal.numero_conta} não encontrada. Salvando...")
            salvar_conta(conta_principal)
            print("-> SUCESSO: Conta salva no banco.")
        else:
            print(f"-> INFO: Conta {conta_principal.numero_conta} já existe no banco.")
            # Atualiza o objeto em memória com os dados do banco
            conta_principal = conta_buscada 

        print("\n--- Testes de Busca e Atualização ---")
        # Teste de buscar ativo
        ativo_teste = buscar_ativo_por_ticker(ativo_exemplo.ticker)
        if ativo_teste:
            print (f"Ativo Encontrado: {ativo_teste}")
        else:
            print (f"Ativo '{ativo_exemplo.ticker}' não encontrado.")
            # (Opcional: adicionar o ativo_exemplo ao banco aqui)

        # Teste de atualizar saldo
        NOVO_SALDO = 123.45 # Um valor de teste
        print(f"\nTestando atualização de saldo para R$ {NOVO_SALDO:.2f}...")
        atualizar_saldo_conta(conta_principal.numero_conta, NOVO_SALDO)
        conta_atualizada = buscar_conta_por_numero(conta_principal.numero_conta)
        
        # CORREÇÃO: Usando seu getter 'saldo_da_conta'
        if conta_atualizada and conta_atualizada.saldo_da_conta == NOVO_SALDO:
            print(f"-> SUCESSO: Saldo atualizado no banco.")
            conta_principal = conta_atualizada # Atualiza o objeto principal em memória
        else:
            print(f"-> FALHA: Saldo não foi atualizado no banco.")

    except (ValueError, mysql.connector.Error, Exception) as e:
        print(f"\n--- ERRO CRÍTICO NA INICIALIZAÇÃO ---")
        print(f"Ocorreu um erro ao carregar dados: {e}")
        print("Aplicação será encerrada.")
        return # Encerra o programa se a inicialização falhar

    # --- FIM DO BLOCO DE INICIALIZAÇÃO ---


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

        # Lógica do Menu
        if opcao == '1':
            print("\n--- Resumo da Conta ---")
            # Usamos o objeto 'conta_principal' atualizado
            conta_principal.exibir_resumo() 
            
        elif opcao == '2':
            try:
                valor_str = input("Digite o valor a ser depositado: R$ ")
                valor_float = float(valor_str)
                
                # 1. Atualiza o objeto em memória
                conta_principal.depositar(valor_float) 
                
                # 2. Salva a mudança no banco de dados
                # CORREÇÃO: Usando seu getter
                atualizar_saldo_conta(conta_principal.numero_conta, conta_principal.saldo_da_conta) 
                
                print("Depósito realizado e salvo no banco.")
                
            except (ValueError, TypeError) as e:
                # CORREÇÃO: Remover 'return', apenas imprimir o erro
                print(f"Erro ao depositar: {e}")

        elif opcao == '3':
            try:
                valor_str = input("Digite o valor a ser sacado: R$ ")
                valor_float = float(valor_str)
                
                # 1. Atualiza o objeto em memória (aqui ocorre a validação de saldo)
                conta_principal.sacar(valor_float)
                
                # 2. Salva a mudança no banco de dados
                # CORREÇÃO: Usando seu getter
                atualizar_saldo_conta(conta_principal.numero_conta, conta_principal.saldo_da_conta)
                
                print("Saque realizado e salvo no banco.")
                
            except (ValueError, TypeError) as e:
                # CORREÇÃO: Remover 'return'
                print(f"Erro ao sacar: {e}")
            
        elif opcao == '4': # CORREÇÃO: Removido o '.'
            print("\n--- Comprar Ativo ---")
            try:
                print("Ativo disponível:")
                print(ativo_exemplo)
                # CORREÇÃO: Usando seu getter
                print(f"Saldo Disponível: R$ {conta_principal.saldo_da_conta:.2f}")
                
                decisao = input("Deseja comprar este ativo? (S/N): ").upper().strip()
                if decisao == 'S':
                    quantidade_str = input(f"Quantos ativos {ativo_exemplo.ticker} deseja comprar? ")
                    quantidade_int = int(quantidade_str)
                    
                    # 1. Atualiza o objeto em memória (valida e muda saldo/carteira)
                    conta_principal.comprar_ativo(ativo_exemplo, quantidade_int)
                    
                    # 2. Salva as mudanças no banco de dados
                    # (Precisaremos de 'atualizar_posicao_carteira' aqui no futuro)
                    # CORREÇÃO: Usando seu getter
                    atualizar_saldo_conta(conta_principal.numero_conta, conta_principal.saldo_da_conta)
                    
                    print("Compra realizada e saldo salvo no banco.")
                    # (A carteira em si ainda não está sendo salva no BD!)
                else:
                    print("Compra cancelada.")
            except (ValueError, TypeError) as e:
                print(f"Erro ao comprar: {e}")
            
        elif opcao == '5':
            print("\n--- Vender Ativo ---")
            try:
                print("Ativos que constam na sua carteira:")
                print(conta_principal.carteira) # Isso ainda é da memória
                
                # (A lógica aqui precisará ser melhorada para buscar o ativo real do BD)
                decisao = input(f"Deseja vender {ativo_exemplo.ticker}? (S/N): ").upper().strip()
                
                if decisao == 'S':
                    quantidade_str = input(f"Quantos ativos {ativo_exemplo.ticker} deseja vender? ")
                    quantidade_int = int(quantidade_str)
                    
                    # 1. Atualiza o objeto em memória
                    conta_principal.vender_ativo(ativo_exemplo, quantidade_int)
                    
                    # 2. Salva as mudanças no banco de dados
                    # (Precisaremos de 'atualizar_posicao_carteira' aqui)
                    # CORREÇÃO: Usando seu getter
                    atualizar_saldo_conta(conta_principal.numero_conta, conta_principal.saldo_da_conta)
                    
                    print("Venda realizada e saldo salvo no banco.")
                    # (A carteira em si ainda não está sendo salva no BD!)
                else:
                    print("Venda cancelada.")
            except (ValueError, TypeError) as e:
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