from .cliente import Cliente
from .ativo import Ativo

class ContaInvestimento:
    def __init__(self, cliente : Cliente, numero_conta : str, saldo_inicial : float = 0.0):
        
        self._cliente = cliente
        self._numero_conta = numero_conta
        self._saldo_disponivel = saldo_inicial
        self._carteira = {}
    
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

    def comprar_ativo(self, ativo_a_comprar : Ativo, quantidade : int):

        if not isinstance (ativo_a_comprar, Ativo):
            raise TypeError ("Precisa ser uma instancia da classe Ativo.")
        if quantidade <= 0:
            raise ValueError ("A quantidade não pode ser menor ou igual a 0.")
        if not isinstance(quantidade, int):
            raise ValueError ("A quantidade deve ser um valor inteiro.")
        
        custo_total = ativo_a_comprar.preco_atual * quantidade

        if custo_total > self._saldo_disponivel:
            raise ValueError("Saldo insuficiente para realizar a compra.")
        
        self._saldo_disponivel = self._saldo_disponivel - custo_total
        
        ticker = ativo_a_comprar.ticker
        if ticker in self._carteira:
            self._carteira[ticker] += quantidade
        else:
            self._carteira[ticker] = quantidade

        print (f'Compra realizada com sucesso!')
        print (f"{self._cliente.nome_cliente} comprou {quantidade}x do ativo {ticker}")

    def vender_ativo(self, ativo_a_vender: Ativo, quantidade: int):

        if not isinstance (ativo_a_vender, Ativo):
            raise TypeError ("Precisa ser uma instancia da classe Ativo.")
        if quantidade <= 0:
            raise ValueError ("A quantidade não pode ser menor ou igual a 0.")
        if not isinstance(quantidade, int):
            raise ValueError ("A quantidade deve ser um valor inteiro.")
        
        ticker = ativo_a_vender.ticker
        
        if ticker not in self._carteira:
            raise ValueError("O ativo não consta na carteira.")
        if quantidade > self._carteira[ticker]:
            raise ValueError("Você não contém a quantidade de ticker para vender.")
        
        valor_da_venda = ativo_a_vender.preco_atual * quantidade
        self._saldo_disponivel += valor_da_venda
        self._carteira[ticker] -= quantidade
        
        if self._carteira[ticker] == 0:
            del self._carteira[ticker] 