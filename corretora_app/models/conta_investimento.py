from .cliente import Cliente

class ContaInvestimento:
    def __init__(self, cliente : Cliente, numero_conta : str, saldo_inicial : float = 0.0):
        
        self._cliente = cliente
        self._numero_conta = numero_conta
        self._saldo_disponivel = saldo_inicial
        self._carteira = {}
    
    def __str__(self):
        
        nome_cliente = self._cliente.nome_cliente
        saldo_formatado = f"R$ {self._saldo_disponivel : .2f}"
        return f"Nome do cliente: {nome_cliente}; Numero da conta: {self._numero_conta}; Saldo disponivel: {saldo_formatado}."
    
    def depositar(self, value: float):
        
        if not isinstance (value, (int, float)):
            raise TypeError("O valor que você deseja depositar, deve ser um digito numérico.")
        
        if value <= 0:
            raise ValueError("O valor que você deseja depositar, não pode ser menor ou igual a 0")
        
        self._saldo_disponivel += value
        print (f'Depósito de R$ {value:.2f} realizado com sucesso.')

    def sacar(self, value : float):
        
        if not isinstance (value, (float, int)):
            raise TypeError ("O valor que você deseja sacar, deve ser um digito numérico.")
        if value <= 0:
            raise ValueError("Não é possivel sacar um valor menor ou igual a zero.")
        if value > self._saldo_disponivel:
            raise ValueError("Saldo insuficiente.")
        
        self._saldo_disponivel -= value
        print(f"Saque de R$ {value:.2f} realizado, seu saldo atual é {self._saldo_disponivel}")

