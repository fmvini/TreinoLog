class GrupoMuscular:
    def __init__(self, nome: str, descricao: str = None, id: int = None):
        self.nome = nome
        self.descricao = descricao
        self.id = id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = valor.strip()

        if not valor:
            raise ValueError("O nome do grupo muscular não pode ser vazio.")

        if len(valor) > 40:
            raise ValueError("O nome do grupo muscular não pode ter mais de 40 caracteres.")

        self._nome = valor

    @property
    def descricao(self) -> str | None:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: str | None) -> None:
        if valor is not None:
            valor = valor.strip()

        self._descricao = valor or None

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, valor: int | None) -> None:
        self._id = valor

    def __str__(self) -> str:
        if self.descricao:
            return f"[{self.id}] {self.nome} - {self.descricao}"
        return f"[{self.id}] {self.nome}"