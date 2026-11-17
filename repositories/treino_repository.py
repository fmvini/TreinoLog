from database import Database
from models.treino import Treino
from exceptions import RegistroNaoEncontradoError


class TreinoRepository:
    def __init__(self, db: Database):
        self.db = db

    def criar(self, treino: Treino) -> Treino:
        cursor = self.db.conexao.execute(
            """
            INSERT INTO treinos (nome, data, duracao_min, observacoes)
            VALUES (?, ?, ?, ?)
            """,
            (treino.nome, treino.data, treino.duracao_min, treino.observacoes)
        )
        treino.id = cursor.lastrowid
        self.db.conexao.commit()
        return treino

    def buscar_por_id(self, id: int) -> Treino:
        cursor = self.db.conexao.execute(
            """
            SELECT id, nome, data, duracao_min, observacoes
            FROM treinos
            WHERE id = ?
            """,
            (id,)
        )
        registro = cursor.fetchone()

        if registro is None:
            raise RegistroNaoEncontradoError(f"Treino com ID {id} não encontrado.")

        return Treino(
            id=registro["id"],
            nome=registro["nome"],
            data=registro["data"],
            duracao_min=registro["duracao_min"],
            observacoes=registro["observacoes"]
        )
    def listar_todos(self) -> list[Treino]:
        cursor = self.db.conexao.execute(
            """
            SELECT id, nome, data, duracao_min, observacoes
            FROM treinos
            """
        )
        registros = cursor.fetchall()

        return [
                Treino(
                id=registro["id"],
                nome=registro["nome"],
                data=registro["data"],
                duracao_min=registro["duracao_min"],
                observacoes=registro["observacoes"]
            )
            for registro in registros
        ]
    def listar_por_periodo(self, data_inicio: str, data_fim: str) -> list[Treino]:
        cursor = self.db.conexao.execute(
            """
            SELECT id, nome, data, duracao_min, observacoes
            FROM treinos 
            WHERE data BETWEEN ? AND ?
            """,
            (data_inicio, data_fim)
        )
        registros = cursor.fetchall()

        return [
            Treino(
                id=registro["id"],
                nome=registro["nome"],
                data=registro["data"],
                duracao_min=registro["duracao_min"],
                observacoes=registro["observacoes"]
            )
            for registro in registros
        ]

    def atualizar(self, treino: Treino) -> None:
        cursor = self.db.conexao.execute(
            """
            UPDATE treinos
            SET nome = ?, data = ?, duracao_min = ?, observacoes = ?
            WHERE id = ?
            """,
            (treino.nome, treino.data, treino.duracao_min, treino.observacoes, treino.id)
        )
        if cursor.rowcount == 0:
            raise RegistroNaoEncontradoError(f"Treino com id {treino.id} não encontrado.")
        self.db.conexao.commit()

    def deletar(self, id: int) -> None:
        cursor = self.db.conexao.execute(
            """
            DELETE FROM treinos
            WHERE id = ?
            """, 
            (id,)
        )
        if cursor.rowcount == 0:
            raise RegistroNaoEncontradoError(f"Treino com o ID {id} não encontrado.")
        self.db.conexao.commit()