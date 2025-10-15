class Cliente:
    def __init__(self, nome_cliente : str, cpf_cliente : str):
        self.nome_cliente = nome_cliente
        self.cpf_cliente = cpf_cliente

    def __str__(self):
        return (f"Cliente: {self.nome_cliente} | CPF, {self.cpf_cliente} ")

    @property
    def nome_cliente (self):
        return self._nome_cliente.title()

    @nome_cliente.setter
    def nome_cliente(self, value: str):
        if not value.strip():
            raise ValueError("O nome do cliente não pode ser vazio.")
        else:
            self._nome_cliente = value.strip()

    @property
    def cpf_cliente(self):
        cpf = self._cpf_cliente
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    @cpf_cliente.setter
    def cpf_cliente(self, value):
        value = value.replace(" ", "").replace("-", "").replace(".", "")
        if not isinstance(value, str):
            raise TypeError("O CPF precisa ser uma string.")
        if len(value) != 11:
            raise ValueError("O CPF inválido: deve ter 11 dígitos numéricos.")
        self._cpf_cliente = value
        