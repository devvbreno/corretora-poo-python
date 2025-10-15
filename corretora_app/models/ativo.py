class Ativo:
    def __init__(self, nome_empresa: str, ticker: str, preco_atual: float):
        self._nome_empresa = nome_empresa
        self._preco_atual = preco_atual
        self._ticker = ticker

    def __str__(self):
        return f"{self._nome_empresa} ({self._ticker}) - Preço: R$ {self._preco_atual}"

    @property  # getter
    def ticker(self):
        return self._ticker

    @ticker.setter  # setter
    def ticker(self, novo_ticker: str):
        if not novo_ticker:
            print("ValueError: O ticker não pode ser vazio.")
        else:
            self._ticker = novo_ticker
