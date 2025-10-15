class Ativo:
    def __init__(self, ticker: str, nome_empresa: str, preco_atual: float):
        self.nome_empresa = nome_empresa
        self.preco_atual = preco_atual
        self.ticker = ticker

    def __str__(self):
        return f"{self.nome_empresa} ({self.ticker}) - Preço: R$ {self.preco_atual}"

	# Getter e Setter do Ticker

    @property
    def ticker(self):
        return self._ticker.upper()

    @ticker.setter
    def ticker(self, novo_ticker: str):
        if not novo_ticker:
            raise ValueError("O ticker não pode ser vazio.")
        else:
            self._ticker = novo_ticker.strip()
      
    # Getter e Setter do Nome da empresa                
       
    @property
    def nome_empresa(self):
        return self._nome_empresa

    @nome_empresa.setter
    def nome_empresa(self, novo_nome_empresa: str):
        if not novo_nome_empresa:
            raise ValueError("O nome_empresa não pode ser vazio.")
        else:
            self._nome_empresa = novo_nome_empresa.strip()

	# Getter e Setter do Preço do ativo

    @property
    def preco_atual (self):
        return self._preco_atual
    
    @preco_atual.setter
    def preco_atual (self, novo_preco : float):
        if not isinstance (novo_preco, (int, float)):
            raise TypeError("O preço não pode ser uma String.")
        if novo_preco < 0:
            raise ValueError("O preço não pode ser um numero negativo.")
        self._preco_atual = novo_preco
            
