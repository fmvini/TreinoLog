from repositories.grupo_muscular_repository import GrupoMuscularRepository
from models.grupo_muscular import GrupoMuscular

class GrupoMuscularService:
    def __init__(self, repository: GrupoMuscularRepository):
        self.repository = repository

    def criar(self, grupo: GrupoMuscular) -> GrupoMuscular:
        if not grupo.nome.strip():
            raise ValueError("O nome do grupo não pode ser vazio")
        if any(
            existente.nome == grupo.nome
            for existente in self.repository.listar_todos()
        ):
            raise ValueError("Já existe um grupo muscular com esse nome.")
        return self.repository.criar(grupo)

    def atualizar(self, grupo: GrupoMuscular) -> GrupoMuscular:
        if not grupo.nome.strip():
            raise ValueError("O nome do grupo não pode ser vazio.")
        if grupo.id is None:
            raise ValueError("O grupo precisa de um ID.")
        if not self.repository.buscar_por_id(grupo.id):
            raise ValueError("O ID do grupo não foi encontrado no banco.")
        if any(
            existente.id != grupo.id and existente.nome == grupo.nome
            for existente in self.repository.listar_todos()
        ):
            raise ValueError("Já existe outro grupo muscular com esse nome.")
        return self.repository.atualizar(grupo)

    def deletar(self, id: int) -> None:
        if not isinstance(id, int) or isinstance(id, bool):
            raise TypeError("O ID deve ser de valor inteiro.")
        if not self.repository.buscar_por_id(id):
            raise ValueError("O ID do grupo não foi encontrado no banco.")
        self.repository.deletar(id)

    def listar(self) -> list[GrupoMuscular]:
        return self.repository.listar_todos()
    def buscar_por_id(self, id: int) -> GrupoMuscular:
        return self.repository.buscar_por_id(id)