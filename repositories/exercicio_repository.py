import sqlite3

from database import Database
from models.exercicio import Exercicio
from exceptions import RegistroNaoEncontradoError, RegraDeNegocioError


class ExercicioRepository:
    def __init__(self, db: Database):
        self.db = db

    def criar(self, exercicio: Exercicio) -> Exercicio:
        cursor = self.db.conexao.execute(
            """
            INSERT INTO exercicios (nome, grupo_id, equipamento)
            VALUES (?, ?, ?)
            """,
            (exercicio.nome, exercicio.grupo_id, exercicio.equipamento)
        )
        exercicio.id = cursor.lastrowid
        self.db.conexao.commit()
        return exercicio

    def buscar_por_id(self, id: int) -> Exercicio:
        cursor = self.db.conexao.execute(
            """
            SELECT
                e.id,
                e.nome,
                e.grupo_id,
                e.equipamento,
                g.nome AS grupo_nome
            FROM exercicios AS e
            INNER JOIN grupos_musculares AS g
                ON e.grupo_id = g.id
            WHERE e.id = ?
            """,
            (id,)
        )

        registro = cursor.fetchone()

        if registro is None:
            raise RegistroNaoEncontradoError(
                f"Exercício com ID {id} não encontrado."
            )

        return Exercicio(
            id=registro["id"],
            nome=registro["nome"],
            grupo_id=registro["grupo_id"],
            equipamento=registro["equipamento"],
            grupo_nome=registro["grupo_nome"]
        )

    def listar_todos(self) -> list[Exercicio]:
        cursor = self.db.conexao.execute(
            """
            SELECT
                e.id,
                e.nome,
                e.grupo_id,
                e.equipamento,
                g.nome AS grupo_nome
            FROM exercicios AS e
            INNER JOIN grupos_musculares AS g
                ON e.grupo_id = g.id
            """
        )
        registros = cursor.fetchall()

        return [
            Exercicio(
            id=registro["id"],
            nome=registro["nome"],
            grupo_id=registro["grupo_id"],
            equipamento=registro["equipamento"],
            grupo_nome=registro["grupo_nome"]
        )
        for registro in registros
    ]

    def listar_por_grupo(self, grupo_id: int) -> list[Exercicio]:
        cursor = self.db.conexao.execute(
            """
            SELECT
                e.id,
                e.nome,
                e.grupo_id,
                e.equipamento,
                g.nome AS grupo_nome
            FROM exercicios AS e
            INNER JOIN grupos_musculares AS g
                ON e.grupo_id = g.id
            WHERE e.grupo_id = ?
            """,
            (grupo_id,)
        )
        registros = cursor.fetchall()

        return [
            Exercicio(
            id=registro["id"],
            nome=registro["nome"],
            grupo_id=registro["grupo_id"],
            equipamento=registro["equipamento"],
            grupo_nome=registro["grupo_nome"]
        )
        for registro in registros
    ]

    def atualizar(self, exercicio: Exercicio) -> None:
        cursor = self.db.conexao.execute(
            """
            UPDATE exercicios
            SET nome = ?, grupo_id = ?, equipamento = ?
            WHERE id = ?
            """,
            (exercicio.nome, exercicio.grupo_id, exercicio.equipamento, exercicio.id)
        )
        if cursor.rowcount == 0:
            raise RegistroNaoEncontradoError(f"Exercicio com o ID {exercicio.id} não encontrado")
        self.db.conexao.commit()

    def deletar(self, id: int) -> None:
        try:
            cursor = self.db.conexao.execute(
                """
                DELETE FROM exercicios
                WHERE id = ?
                """,
                (id,)
            )
        except sqlite3.IntegrityError as erro:
            self.db.conexao.rollback()
            raise RegraDeNegocioError(
                "Não é possível excluir este exercício porque ele está associado a uma ou mais séries."
            ) from erro
        if cursor.rowcount == 0:
            raise RegistroNaoEncontradoError(f"Exercicio com o ID {id} não encontrado.")
        self.db.conexao.commit()