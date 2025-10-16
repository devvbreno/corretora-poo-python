from .cliente import Cliente
from .itransacionavel import ITransacionavel

#Classe abstrata mãe (define a estrutura de uma conta genérica)

class Conta(ITransacionavel):
    def __init__(self, cliente : Cliente, numero_conta : str, saldo_inicial : float = 0.0):
        
        self._cliente = cliente
        self._numero_conta = numero_conta
        self._saldo_disponivel = saldo_inicial

    def __str__(self):
        
        nome_cliente = self._cliente.nome_cliente
        saldo_formatado = f"R$ {self.saldo_da_conta : .2f}"
        return f"\n Cliente: {nome_cliente} | Conta: {self._numero_conta} | Saldo disponivel: {saldo_formatado}."

    @property
    def saldo_da_conta (self):
        return self._saldo_disponivel
    
    @property
    def carteira(self):
        return self._carteira.copy()
    
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
    
    def exibir_resumo(self):
        print(f"Resumo da Conta: {self._numero_conta}")
        print (f"Saldo Disponível: R$ {self.saldo_da_conta:.2f}")