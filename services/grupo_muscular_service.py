from repositories.grupo_muscular_repository import GrupoMuscularRepository
from models.grupo_muscular import GrupoMuscular

class GrupoMuscularService:
    def __init__(self, repository: GrupoMuscularRepository):
        self.repository = repository

    def criar(self, grupo: GrupoMuscular) -> GrupoMuscular:
        if not grupo.nome.strip():
            raise ValueError("O nome do grupo não pode ser vazio")
        return self.repository.criar(grupo)

    def atualizar(self, grupo: GrupoMuscular) -> GrupoMuscular:
        if not grupo.nome.strip():
            raise ValueError("O nome do grupo não pode ser vazio.")
        if grupo.id is None:
            raise ValueError("O grupo precisa de um ID.")
        if not self.repository.buscar_por_id(grupo.id):
            raise ValueError("O ID do grupo não foi encontrado no banco.")
        return self.repository.atualizar(grupo)

    def deletar(self, id: int) -> None:
        if not isinstance(id, int) or isinstance(id, bool):
            raise TypeError("O ID deve ser de valor inteiro.")
        if not self.repository.buscar_por_id(id):
            raise ValueError("O ID do grupo não foi encontrado no banco.")
        self.repository.deletar(id)
