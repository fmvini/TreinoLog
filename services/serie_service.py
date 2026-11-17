from repositories.serie_repository import SerieRepository
from repositories.treino_repository import TreinoRepository
from repositories.exercicio_repository import ExercicioRepository

from models.serie import Serie


class SerieService:
    def __init__(
        self,
        serie_repository: SerieRepository,
        treino_repository: TreinoRepository,
        exercicio_repository: ExercicioRepository
    ):
        self.serie_repository = serie_repository
        self.treino_repository = treino_repository
        self.exercicio_repository = exercicio_repository

    def criar(self, serie: Serie) -> Serie:
        if serie.treino_id is None:
            raise ValueError("O treino_id precisa ser informado.")
        if not self.treino_repository.buscar_por_id(serie.treino_id):
            raise ValueError("O treino associado precisa existir.")
        if serie.exercicio_id is None:
            raise ValueError("O exercicio_id precisa ser informado")
        if not self.exercicio_repository.buscar_por_id(serie.exercicio_id):
            raise ValueError("O exercicio associado precisa existir")
        if not isinstance(serie.numero_serie, int) or isinstance(serie.numero_serie, bool):
            raise TypeError("O numero_serie deve ser um inteiro positivo.")
        if serie.numero_serie <= 0:
            raise ValueError("O número da série deve ser maior que 0.")
        if not isinstance(serie.repeticoes, int) or isinstance(serie.repeticoes, bool):
            raise TypeError("O numero de repetições precisa ser um numero inteiro")
        if serie.repeticoes <= 0:
            raise ValueError("O numero de repetições deve ser maior do que 0")
        if not isinstance(serie.carga_kg, (int, float)) or isinstance(serie.carga_kg, bool):
            raise TypeError("A carga deve ser um numero inteiro ou decimal.")
        if serie.carga_kg < 0:
            raise ValueError("A carga não pode ser negativa.")
        return self.serie_repository.criar(serie)

    def atualizar(self, serie: Serie) -> Serie:
        if serie.treino_id is None:
            raise ValueError("O treino_id precisa ser informado.")
        if not self.treino_repository.buscar_por_id(serie.treino_id):
            raise ValueError("O treino associado precisa existir.")
        if serie.exercicio_id is None:
            raise ValueError("O exercicio_id precisa ser informado")
        if not self.exercicio_repository.buscar_por_id(serie.exercicio_id):
            raise ValueError("O exercicio associado precisa existir")
        if not isinstance(serie.numero_serie, int) or isinstance(serie.numero_serie, bool):
            raise TypeError("O numero_serie deve ser um inteiro positivo.")
        if serie.numero_serie <= 0:
            raise ValueError("O número da série deve ser maior que 0.")
        if not isinstance(serie.repeticoes, int) or isinstance(serie.repeticoes, bool):
            raise TypeError("O numero de repetições precisa ser um numero inteiro")
        if serie.repeticoes <= 0:
            raise ValueError("O numero de repetições deve ser maior do que 0")
        if not isinstance(serie.carga_kg, (int, float)) or isinstance(serie.carga_kg, bool):
            raise TypeError("A carga deve ser um numero inteiro ou decimal.")
        if serie.carga_kg < 0:
            raise ValueError("A carga não pode ser negativa.")
        if serie.id is None:
            raise ValueError("O ID da serie deve ser informado.")
        if not self.serie_repository.buscar_por_id(serie.id):
            raise ValueError("Serie não encontrada no banco de dados.")
        return self.serie_repository.atualizar(serie)

    def deletar(self, id: int) -> None:
        if not isinstance(id, int) or isinstance(id, bool):
            raise TypeError("O ID precisa ser um valor inteiro.")
        if not self.serie_repository.buscar_por_id(id):
            raise ValueError("O ID informado não foi encontrado no banco de dados.")
        self.serie_repository.deletar(id)