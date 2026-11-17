from database import Database
from models.serie import Serie
from exceptions import RegistroNaoEncontradoError


class SerieRepository:
    def __init__(self, db: Database):
        self.db = db

    def criar(self, serie: Serie):
        cursor = self.db.conexao.execute(
            """
            INSERT INTO series (treino_id, exercicio_id, numero_serie, repeticoes, carga_kg)
            VALUES (?, ?, ?, ?, ?)
            """,
            (serie.treino_id, serie.exercicio_id, serie.numero_serie, serie.repeticoes, serie.carga_kg)
        )
        serie.id = cursor.lastrowid
        self.db.conexao.commit()
        return serie

    def buscar_por_id(self, id: int) -> Serie:
        cursor = self.db.conexao.execute(
            """
            SELECT
                s.id,
                s.treino_id,
                s.exercicio_id,
                s.numero_serie,
                s.repeticoes,
                s.carga_kg,
                e.nome AS exercicio_nome
            FROM series AS s
            INNER JOIN exercicios AS e
                ON s.exercicio_id = e.id
            WHERE s.id = ?
            """,
            (id,)
        )
        registro = cursor.fetchone()
        if registro is None:
            raise RegistroNaoEncontradoError(f"Serie com ID {id} não encontrada.")
        return Serie(
            id=registro["id"],
            treino_id=registro["treino_id"],
            exercicio_id=registro["exercicio_id"],
            numero_serie=registro["numero_serie"],
            repeticoes=registro["repeticoes"],
            carga_kg=registro["carga_kg"],
            exercicio_nome=registro["exercicio_nome"]
        )
    def listar_todos(self) -> list[Serie]:
        cursor = self.db.conexao.execute(
            """
            SELECT
                s.id,
                s.treino_id,
                s.exercicio_id,
                s.numero_serie,
                s.repeticoes,
                s.carga_kg,
                e.nome AS exercicio_nome
            FROM series AS s
            INNER JOIN exercicios AS e
                ON s.exercicio_id = e.id
            ORDER BY s.treino_id, s.exercicio_id, s.numero_serie
            """
        )
        registros = cursor.fetchall()
        return [
            Serie(
                id=registro["id"],
                treino_id=registro["treino_id"],
                exercicio_id=registro["exercicio_id"],
                numero_serie=registro["numero_serie"],
                repeticoes=registro["repeticoes"],
                carga_kg=registro["carga_kg"],
                exercicio_nome=registro["exercicio_nome"]
                )
            for registro in registros
            ]
    def listar_por_treino(self, treino_id: int) -> list[Serie]:
        cursor = self.db.conexao.execute(
            """
            SELECT
                s.id,
                s.treino_id,
                s.exercicio_id,
                s.numero_serie,
                s.repeticoes,
                s.carga_kg,
                e.nome AS exercicio_nome
            FROM series AS s
            INNER JOIN exercicios AS e
                ON s.exercicio_id = e.id
            WHERE s.treino_id = ?
            ORDER BY s.exercicio_id, s.numero_serie""",
            (treino_id,)
        )
        registros = cursor.fetchall()
        return [
            Serie(
                id=registro["id"],
                treino_id=registro["treino_id"],
                exercicio_id=registro["exercicio_id"],
                numero_serie=registro["numero_serie"],
                repeticoes=registro["repeticoes"],
                carga_kg=registro["carga_kg"],
                exercicio_nome=registro["exercicio_nome"]
                )
            for registro in registros
            ]
    def listar_por_exercicio(self, exercicio_id: int) -> list[Serie]:
        cursor = self.db.conexao.execute(
            """
            SELECT
                s.id,
                s.treino_id,
                s.exercicio_id,
                s.numero_serie,
                s.repeticoes,
                s.carga_kg,
                e.nome AS exercicio_nome
            FROM series AS s
            INNER JOIN exercicios AS e
                ON s.exercicio_id = e.id
            WHERE s.exercicio_id = ?
            ORDER BY s.treino_id, s.numero_serie
            """,
            (exercicio_id,)
        )
        registros = cursor.fetchall()
        return [
            Serie(
                id=registro["id"],
                treino_id=registro["treino_id"],
                exercicio_id=registro["exercicio_id"],
                numero_serie=registro["numero_serie"],
                repeticoes=registro["repeticoes"],
                carga_kg=registro["carga_kg"],
                exercicio_nome=registro["exercicio_nome"]
                )
            for registro in registros
            ]

    def atualizar(self, serie: Serie) -> None:
       cursor = self.db.conexao.execute("""
            UPDATE series
            SET treino_id = ?,
                exercicio_id = ?,
                numero_serie = ?,
                repeticoes = ?,
                carga_kg = ?
            WHERE id = ?
            """, 
            (serie.treino_id, serie.exercicio_id, serie.numero_serie, serie.repeticoes, serie.carga_kg, serie.id)
        )
       if cursor.rowcount == 0:
           raise RegistroNaoEncontradoError(f"Serie com ID {serie.id} não encontrada.")
       self.db.conexao.commit()

    def deletar(self, id: int) -> None:
        cursor = self.db.conexao.execute("""
            DELETE FROM series
            WHERE id = ?
            """,
            (id,)                                 
            )
        if cursor.rowcount == 0:
            raise RegistroNaoEncontradoError(f"Serie com ID {id} não encontrada.")
        self.db.conexao.commit()
