from repositories.exercicio_repository import ExercicioRepository
from models.exercicio import Exercicio
from repositories.grupo_muscular_repository import GrupoMuscularRepository

class ExercicioService:
    def __init__(
    self,
    repository: ExercicioRepository,
    grupo_repository: GrupoMuscularRepository
    ):
        self.repository = repository
        self.grupo_repository = grupo_repository

    def criar(self, exercicio: Exercicio) -> Exercicio:
        if not exercicio.nome.strip():
            raise ValueError("O nome do exercicio não pode ser vazio.")
        if exercicio.grupo_id is None:
            raise ValueError("O grupo_id não pode ser vazio.")
        if not self.grupo_repository.buscar_por_id(exercicio.grupo_id):
            raise ValueError("O grupo muscular informado não foi encontrado.")
        return self.repository.criar(exercicio)

    def atualizar(self, exercicio: Exercicio) -> Exercicio:
        if not exercicio.nome.strip():
            raise ValueError("O nome do exercicio não pode ser vazio.")
        if exercicio.id is None:
            raise ValueError("O ID não pode ser vazio.")
        if exercicio.grupo_id is None:
            raise ValueError("O grupo id não pode ser vaizio")
        if not self.grupo_repository.buscar_por_id(exercicio.grupo_id):
            raise ValueError("O grupo muscular informado não foi encontrado.")
        if not self.repository.buscar_por_id(exercicio.id):
            raise ValueError("O exercício informado não foi encontrado.")
        return self.repository.atualizar(exercicio)        

    def deletar(self, id: int) -> None:
        if not isinstance(id, int) or isinstance(id, bool):
            raise TypeError("O ID deve ser um valor inteiro.")
        if not self.repository.buscar_por_id(id):
            raise ValueError("O exercício informado não foi encontrado.")
        self.repository.deletar(id)