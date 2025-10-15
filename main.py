from corretora_app.models.conta import Conta
from corretora_app.models.ativo import Ativo
from corretora_app.models.cliente import Cliente
from corretora_app.models.conta_investimento import ContaInvestimento


# primeira fase
print("--- [1: Criação de Objetos] ---")
try:
    ativo1 = Ativo(ticker="  pETr4  ", nome_empresa="  petrobrás s.a  ", preco_atual=35.20)
    ativo2 = Ativo(ticker="  ValE3  ", nome_empresa="  vale s.a  ", preco_atual=67.20)

    cliente1 = Cliente(nome_cliente="   breno elias", cpf_cliente="123.456.789-00")
    conta_do_breno = ContaInvestimento(cliente=cliente1, numero_conta='11111-2')
    
    print("Objetos criados com sucesso!")
    print(ativo1)
    print(cliente1)
    print(conta_do_breno)
except Exception as e:
    print(f"ERRO INESPERADO NA CRIAÇÃO: {e}")

# 2. Testando métodos básicos (Herança)
print("\n--- [2. Testando Métodos Herdados] ---")
print(f"Saldo ANTES: {conta_do_breno}")
conta_do_breno.depositar(1000.00) # Testando o depositar() herdado
conta_do_breno.sacar(100.00)     # Testando o sacar() herdado
print(f"Saldo DEPOIS (depósito de 1000, saque de 100): {conta_do_breno}")


# 3. Testando Métodos da ContaInvestimento
print("\n--- [3. Testando Compra e Venda de Ativos] ---")
# Teste de compra
print("\nRealizando compra de 10x PETR4...")
conta_do_breno.comprar_ativo(ativo1, 10) 
print(f"Conta após a compra: {conta_do_breno}")
print(f"Carteira após a compra: {conta_do_breno.carteira}")

# Teste de venda
print("\nRealizando venda de 4x PETR4...")
conta_do_breno.vender_ativo(ativo1, 4) 
print(f"Conta após a venda: {conta_do_breno}")
print(f"Carteira após a venda: {conta_do_breno.carteira}")

# Teste de venda total
print("\nRealizando venda do restante (6x PETR4)...")
conta_do_breno.vender_ativo(ativo1, 6)
print(f"Conta após zerar a posição: {conta_do_breno}")
print(f"Carteira após zerar a posição (deve estar vazia): {conta_do_breno.carteira}")


# 4. Testando Casos de Erro
print("\n--- [4. Testando Casos de Erro] ---")
# Teste de saque com saldo insuficiente
try:
    print("\nTestando saque com saldo insuficiente...")
    conta_do_breno.sacar(99999.00)
except ValueError as e:
    print(f"-> SUCESSO: Erro esperado capturado: '{e}'")

# Teste de venda de ativo que não possui
try:
    print("\nTestando vender um ativo que não possui (VALE3)...")
    conta_do_breno.vender_ativo(ativo2, 1)
except ValueError as e:
    print(f"-> SUCESSO: Erro esperado capturado: '{e}'")


# 5. Testando o Polimorfismo
print("\n--- [5. Testando o Polimorfismo] ---")

# Criando uma conta genérica (mãe) para comparação
cliente_generico = Cliente(nome_cliente="Cliente Teste", cpf_cliente="99988877766")
conta_simples = Conta(cliente=cliente_generico, numero_conta="00000-0", saldo_inicial=150.0)

print("\n1. Chamando o resumo da Conta Simples (Mãe):")
conta_simples.exibir_resumo()

print("\n2. Chamando o MESMO método na Conta de Investimentos (Filha):")
# Usando a conta_do_breno que já tem saldo e carteira
conta_do_breno.exibir_resumo()