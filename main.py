from corretora_app.models.cliente import Cliente
from corretora_app.models.conta_investimento import ContaInvestimento
from corretora_app.models.ativo import Ativo
from corretora_app.models.conta import Conta 

def main():
    print("--- Bem-vindo(a) à Corretora POO ---")

    # DADOS EM MEMÓRIA (Substitui o Banco de Dados por enquanto)
    try:
        cliente_principal = Cliente(nome_cliente="Breno", cpf_cliente="11122233344")
        conta_principal = ContaInvestimento(cliente=cliente_principal, numero_conta="12345-6")
        ativo_exemplo = Ativo(ticker="PYTH4", nome_empresa="Python Corp", preco_atual=50.0)
        print("Dados iniciais carregados.")
        print(conta_principal)
    except Exception as e:
        print(f"Erro ao inicializar dados: {e}")
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
            
        elif opcao == '4':
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