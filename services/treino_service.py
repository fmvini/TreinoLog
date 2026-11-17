from repositories.treino_repository import TreinoRepository
from models.treino import Treino


class TreinoService:
    def __init__(self, repository: TreinoRepository):
        self.repository = repository

    def criar(self, treino: Treino) -> Treino:
        if not treino.nome.strip():
            raise ValueError("O nome do treino não pode ser vazio.")
        if treino.data is None:
            raise ValueError("A data do treino deve ser informada.")
        if not isinstance(treino.duracao_min, int) or isinstance(treino.duracao_min, bool):
            raise TypeError("A duração precisa ser um número inteiro.")
        if treino.duracao_min <= 0:
            raise ValueError("A duração precisa ser positiva.")
        return self.repository.criar(treino)

    def atualizar(self, treino: Treino) -> Treino:
        if not treino.nome.strip():
            raise ValueError("O nome do treino não pod ser vazio.")
        if treino.id is None:
            raise ValueError("O ID precisa ser informado.")
        if not self.repository.buscar_por_id(treino.id):
            raise ValueError("O treino de id informado não existe no banco")
        if treino.data is None:
            raise ValueError("A data precisa estar informada.")
        if not isinstance(treino.duracao_min, int) or isinstance(treino.duracao_min, bool):
            raise TypeError("A duração precisa ser um número inteiro.")
        if treino.duracao_min <= 0:
            raise ValueError("A duração precisa ser positiva.")
        return self.repository.atualizar(treino)

    def deletar(self, id: int) -> None:
        if not isinstance(id, int) or isinstance(id, bool):
            raise TypeError("O ID precisa ser um numero inteiro.")
        if not self.repository.buscar_por_id(id):
            raise ValueError("O treino de id informado não existe no banco.")
        self.repository.deletar(id)
        
    def listar(self) -> list[Treino]:
        return self.repository.listar_todos()

    def buscar_por_id(self, id: int) -> Treino:
        return self.repository.buscar_por_id(id)