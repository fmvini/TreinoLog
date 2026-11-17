from database import Database
from models.grupo_muscular import GrupoMuscular
from exceptions import RegistroNaoEncontradoError

class GrupoMuscularRepository:
    def __init__(self, db: Database):
        self.db = db

    def criar(self, grupo: GrupoMuscular) -> GrupoMuscular:
        cursor = self.db.conexao.execute(
            """
            INSERT INTO grupos_musculares (nome, descricao)
            VALUES (?, ?)
            """,
            (grupo.nome, grupo.descricao)
        )
        self.db.conexao.commit()
        grupo.id = cursor.lastrowid
        return grupo

    def buscar_por_id(self, id: int) -> GrupoMuscular:
        cursor = self.db.conexao.execute(
            """
            SELECT id, nome, descricao
            FROM grupos_musculares
            WHERE id = ?
            """,
            (id,)
        )
        registro = cursor.fetchone()
        if registro is None:
            raise RegistroNaoEncontradoError(
                f"Grupo muscular com ID {id} não encontrado."
            )
        return GrupoMuscular(
            id=registro["id"],
            nome=registro["nome"],
            descricao=registro["descricao"]
        )
    
    def listar_todos(self) -> list[GrupoMuscular]:
        cursor = self.db.conexao.execute(
            """
            SELECT id, nome, descricao
            FROM grupos_musculares
            ORDER BY nome
            """
        )
        registros = cursor.fetchall()
        return [
            GrupoMuscular(
                id=registro["id"],
                nome=registro["nome"],
                descricao=registro["descricao"]
            )
            for registro in registros
        ]

    def atualizar(self, grupo: GrupoMuscular) -> None:
        cursor = self.db.conexao.execute(
            """
            UPDATE grupos_musculares
            SET nome = ?, descricao = ?
            WHERE id = ?
            """,
            (grupo.nome, grupo.descricao, grupo.id)
        )
        if cursor.rowcount == 0:
            raise RegistroNaoEncontradoError(
                f"Grupo muscular com ID {grupo.id} não encontrado."
            )
        self.db.conexao.commit()

    def deletar(self, id: int) -> None:
        try:
            self.db.conexao.execute(
                """
                DELETE FROM series
                WHERE exercicio_id IN (
                    SELECT id FROM exercicios WHERE grupo_id = ?
                )
                """,
                (id,)
            )
            self.db.conexao.execute(
                "DELETE FROM exercicios WHERE grupo_id = ?",
                (id,)
            )
            cursor = self.db.conexao.execute(
                """
                DELETE FROM grupos_musculares
                WHERE id = ?
                """,
                (id,)
            )
            if cursor.rowcount == 0:
                raise RegistroNaoEncontradoError(
                    f"Grupo muscular com ID {id} não encontrado."
                )
            self.db.conexao.commit()
        except Exception:
            self.db.conexao.rollback()
            raise