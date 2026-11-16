class Exercicio:
    def __init__(self, nome: str, grupo_id: int, equipamento: str = None, id: int = None, grupo_nome: str = None):
        self.nome = nome
        self.grupo_id = grupo_id
        self.equipamento = equipamento
        self.id = id
        self.grupo_nome = grupo_nome

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = valor.strip()

        if not valor:
            raise ValueError("O nome do exercício não pode ser vazio.")

        if len(valor) > 60:
            raise ValueError("O nome do exercício não pode ter mais de 60 caracteres.")

        self._nome = valor

    @property
    def grupo_id(self) -> int:
        return self._grupo_id

    @grupo_id.setter
    def grupo_id(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("O ID do grupo deve ser um inteiro.")

        if valor <= 0:
            raise ValueError("O ID do grupo não pode ser zero ou negativo.")

        self._grupo_id = valor

    @property
    def equipamento(self) -> str | None:
        return self._equipamento

    @equipamento.setter
    def equipamento(self, valor: str | None) -> None:
        if valor is not None:
            valor = valor.strip()

        self._equipamento = valor or None

    def __str__(self) -> str:
        resposta = f"[{self.id}] {self.nome} "
        if self.equipamento:
            resposta += f"({self.equipamento})"
        if self.grupo_nome:
            resposta += f" - {self.grupo_nome}"
        return resposta

        