from corretora_app.models.ativo import Ativo
from corretora_app.models.cliente import Cliente
from corretora_app.models.conta_investimento import ContaInvestimento


print("--- [FASE 1: Criação de Objetos] ---")
try:
    # Testando a normalização de dados nos setters ao criar os objetos
    ativo1 = Ativo(ticker="  pETr4  ", nome_empresa="  petrobrás s.a  ", preco_atual=35.20)
    ativo2 = Ativo(ticker="  Val3  ", nome_empresa="  vale s.a  ", preco_atual=67.20)

    cliente1 = Cliente(nome_cliente="   breno elias", cpf_cliente="123.456.789-00")
    conta_do_breno = ContaInvestimento(cliente=cliente1, numero_conta='11111-2')
    
    print("Objetos criados com sucesso!")
    print(ativo1)   # Deve mostrar o ticker em maiúsculas e o nome formatado
    print(cliente1) # Deve mostrar o nome formatado e o CPF limpo
    print(conta_do_breno) # Deve mostrar o saldo inicial R$ 0.00
except Exception as e:
    print(f"ERRO INESPERADO NA CRIAÇÃO: {e}")

print("\n--- [FASE 2: Testando o Método depositar()] ---")

# Teste de depósito válido
print("\n1. Testando depósito válido:")
print(f"Saldo ANTES: {conta_do_breno}")
conta_do_breno.depositar(500.50) # Chamamos o método diretamente
print(f"Saldo DEPOIS: {conta_do_breno}")

# Teste de depósito com valor negativo
try:
    print("\n2. Testando depósito com valor negativo (-100):")
    conta_do_breno.depositar(-100)
except ValueError as e:
    print(f"-> SUCESSO: Erro esperado capturado: '{e}'")
print(f"Saldo não deve ter mudado: {conta_do_breno}")

# Teste de depósito com tipo inválido
try:
    print("\n3. Testando depósito com texto:")
    conta_do_breno.depositar("mil reais")
except TypeError as e:
    print(f"-> SUCESSO: Erro esperado capturado: '{e}'")
print(f"Saldo não deve ter mudado: {conta_do_breno}")


print("\n--- [FASE 3: Testando o Método sacar()] ---")

# Teste de saque válido
print("\n1. Testando saque válido (R$ 100.25):")
print(f"Saldo ANTES: {conta_do_breno}")
conta_do_breno.sacar(100.25)
print(f"Saldo DEPOIS: {conta_do_breno}")

# Teste de saque com saldo insuficiente
try:
    print("\n2. Testando saque maior que o saldo (R$ 9999.00):")
    conta_do_breno.sacar(9999.00)
except ValueError as e:
    print(f"-> SUCESSO: Erro esperado capturado: '{e}'")
print(f"Saldo não deve ter mudado: {conta_do_breno}")

# Teste de saque com valor negativo
try:
    print("\n4. Testando saque com valor negativo (-50):")
    conta_do_breno.sacar(-50)
except ValueError as e:
    print(f"-> SUCESSO: Erro esperado capturado: '{e}'")
print(f"Saldo não deve ter mudado: {conta_do_breno}")

#Teste de compra de ativo valido;

print("\nTestando o método comprar_ativo() ")
print(f"Estado ANTES da compra: {conta_do_breno}")
print(f"Carteira ANTES: {conta_do_breno.carteira}")

print("\nRealizando compra de 5x PETR4...")
conta_do_breno.comprar_ativo(ativo1, 5) 

print("\nEstado DEPOIS da compra:")
print(f"Conta: {conta_do_breno}")
print(f"Carteira: {conta_do_breno.carteira}")

#Teste de venda de ativo valido

print("\nTestando o método vender_ativo() ")
print(f"Estado ANTES da venda: {conta_do_breno}")
print(f"Carteira ANTES: {conta_do_breno.carteira}")

print("\nRealizando venda de 3x PETR4...")
conta_do_breno.vender_ativo(ativo1, 3) 

print("\nEstado DEPOIS da venda:")
print(f"Conta: {conta_do_breno}")
print(f"Carteira: {conta_do_breno.carteira}")

#Teste de vender um ativo que não possui

try:
    print("\nTestando vender um ativo que nao possui:")
    conta_do_breno.vender_ativo(ativo2, 1)
except ValueError as e:
    print(f"-> SUCESSO: Erro esperado capturado: '{e}'")
print(f"Saldo não deve ter mudado: {conta_do_breno}")

#Teste de vender mais ativos do que tem

try:
    print("\nTestando vender mais ativos do que há na carteira:")
    conta_do_breno.vender_ativo(ativo1, 6)
except ValueError as e:
    print(f"-> SUCESSO: Erro esperado capturado: '{e}'")
print(f"Saldo não deve ter mudado: {conta_do_breno}")

# Tentando vender tudo na carteira para saber se zera a posição do ativo (ver se ele some da carteira)
print("\nTestando vender TUDO de um ativo que possui:")
conta_do_breno.vender_ativo(ativo1, 2)
print(f"O ativo deve ter sumido da carteira | Carteira: {conta_do_breno.carteira}")
