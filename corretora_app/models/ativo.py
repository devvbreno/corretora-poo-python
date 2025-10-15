class Ativo:
    def __init__(self, ticker: str, nome_empresa: str, preco_atual: float):
        self._nome_empresa = nome_empresa
        self._preco_atual = preco_atual
        self._ticker = ticker

    def __str__(self):
        return f"{self._nome_empresa} ({self._ticker}) - Preço: R$ {self._preco_atual}"

	# Getter e Setter do Ticker

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, novo_ticker: str):
        if not novo_ticker:
            raise ValueError("O ticker não pode ser vazio.")
        else:
            self._ticker = novo_ticker
            
    # Getter e Setter do Nome da empresa                
            
    @property
    def nome_empresa(self):
        return self._nome_empresa
    
    @nome_empresa.setter
    def nome_empresa(self, novo_nome_empresa: str):
        if not novo_nome_empresa:
            raise ValueError("O nome_empresa não pode ser vazio.")
        else:
            self._nome_empresa = novo_nome_empresa

	# Getter e Setter do Preço do ativo

    @property
    def preco_total (self):
        return self._preco_atual
    
    @preco_total.setter
    def preco_total (self, novo_preco : float):
        if isinstance (novo_preco, (int, float)) or novo_preco < 0:
            raise ValueError("O preço não pode ser um numero negativo ou uma String")
        else:
            self._preco_total = novo_preco
            