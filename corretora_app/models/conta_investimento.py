from .cliente import Cliente
from .ativo import Ativo
from .conta import Conta

class ContaInvestimento(Conta):
    def __init__(self, cliente : Cliente, numero_conta: str, saldo_inicial : float = 0.0, id_conta: int = None ):
        super().__init__(cliente, numero_conta, saldo_inicial, id_conta)
        self._carteira = {}
    
    def __str__(self):
        
        info_base = super().__str__()
        info_carteira = f"| Carteira: {self.carteira}"
        return info_base + info_carteira
    
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
        
        print(f"Venda de {quantidade}x {ticker} realizada com sucesso!")

    def exibir_resumo(self):
        super().exibir_resumo()
        print (f"   Carteira de ativos: {self.carteira}")