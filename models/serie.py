class Serie:
    def __init__(
        self,
        treino_id: int,
        exercicio_id: int,
        numero_serie: int,
        repeticoes: int,
        carga_kg: int | float,
        id: int = None,
        exercicio_nome: str = None
    ):
        self.treino_id = treino_id
        self.exercicio_id = exercicio_id
        self.numero_serie = numero_serie
        self.repeticoes = repeticoes
        self.carga_kg = carga_kg
        self.id = id
        self.exercicio_nome = exercicio_nome

    @property 
    def treino_id(self) -> int:
        return self._treino_id
    @treino_id.setter
    def treino_id(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("O ID de treino deve ser um numero inteiro.")
        if valor <= 0:
            raise ValueError("O ID de treino deve ser um numero positivo")
        self._treino_id = valor

    @property
    def exercicio_id(self) -> int:
        return self._exercicio_id
    @exercicio_id.setter
    def exercicio_id(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("O ID do exercicio deve ser um numero inteiro.")
        if valor <= 0:
            raise ValueError("O ID do exercicio deve ser um valor positivo")
        self._exercicio_id = valor

    @property 
    def numero_serie(self) -> int:
        return self._numero_serie
    @numero_serie.setter
    def numero_serie(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("O numero de series deve ser um numero inteiro.")
        if valor <= 0:
            raise ValueError("O numero de series deve ser maior que 0.")
        self._numero_serie = valor

    @property
    def repeticoes(self) -> int:
        return self._repeticoes
    @repeticoes.setter
    def repeticoes(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("A quantidade de repetições deve ser um numero inteiro.")
        if valor <= 0:
            raise ValueError("A quantidade de repetições deve ser maior que 0")
        self._repeticoes = valor

    @property
    def carga_kg(self) -> int | float:
        return self._carga_kg
    @carga_kg.setter
    def carga_kg(self, valor: int | float) -> None:
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise TypeError("A carga deve ser ser um numero int ou float.")
        if valor < 0:
            raise ValueError("A carga não pode ser menor do que 0.")
        self._carga_kg = valor

    @property 
    def id(self) -> int | None:
        return self._id
    @id.setter
    def id(self, valor: int | None) -> None:
        self._id = valor

    @property
    def exercicio_nome(self) -> str | None:
        return self._exercicio_nome
    @exercicio_nome.setter
    def exercicio_nome(self, valor: str) -> None:
        if valor is not None:
            valor = valor.strip()
        self._exercicio_nome = valor or None

    @property
    def rm_estimado(self) -> float:
        return self.calcular_1rm()

    def calcular_1rm(self) -> float:
        return self.carga_kg * (1 + (self.repeticoes / 30))  

    @property
    def volume(self) -> int | float:
        return self.carga_kg * self.repeticoes      

    def __str__(self) -> str:
        resposta = f"[{self.id}] "
        if self.exercicio_nome:
            resposta += self.exercicio_nome
        resposta += f" - Série {self.numero_serie}: {self.repeticoes} repetições com {self.carga_kg} kg"
        return resposta
        
