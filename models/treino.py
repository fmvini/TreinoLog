from datetime import datetime, date

class Treino:
    def __init__(
        self,
        nome: str,
        data: str,
        duracao_min: int = None,
        observacoes: str = None,
        id: int = None
    ):
        self.nome = nome
        self.data = data
        self.duracao_min = duracao_min
        self.observacoes = observacoes
        self.id = id

    @property
    def nome(self) -> str:
        return self._nome
    @nome.setter
    def nome(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("O nome do treino não pode ser vazio.")
        if len(valor) > 60:
            raise ValueError("O nome do treino não pode ter mais de 60 caracteres")

        self._nome = valor

    @property
    def data(self) -> str:
        return self._data
    @data.setter
    def data(self, valor: str) -> None:
        try: 
            data = datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Data inválida. Use AAAA-MM-DD.")
        if data.date() > date.today():
            raise ValueError("A data do treino não pode ser futura.")
        
        self._data = valor