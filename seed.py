from datetime import date

from database import Database
from models.exercicio import Exercicio
from models.grupo_muscular import GrupoMuscular
from models.serie import Serie
from models.treino import Treino
from repositories.exercicio_repository import ExercicioRepository
from repositories.grupo_muscular_repository import GrupoMuscularRepository
from repositories.serie_repository import SerieRepository
from repositories.treino_repository import TreinoRepository
from services.exercicio_service import ExercicioService
from services.grupo_muscular_service import GrupoMuscularService
from services.serie_service import SerieService
from services.treino_service import TreinoService


def carregar_dados_exemplo() -> None:
    db = Database()

    try:
        db.criar_tabelas()

        grupo_repository = GrupoMuscularRepository(db)
        exercicio_repository = ExercicioRepository(db)
        treino_repository = TreinoRepository(db)
        serie_repository = SerieRepository(db)

        if any((
            grupo_repository.listar_todos(),
            exercicio_repository.listar_todos(),
            treino_repository.listar_todos(),
            serie_repository.listar_todos()
        )):
            print("O banco já contém dados. Nenhum exemplo foi adicionado.")
            return

        grupo_service = GrupoMuscularService(grupo_repository)
        exercicio_service = ExercicioService(
            exercicio_repository,
            grupo_repository
        )
        treino_service = TreinoService(treino_repository)
        serie_service = SerieService(
            serie_repository,
            treino_repository,
            exercicio_repository
        )

        peito = grupo_service.criar(GrupoMuscular("Peito", "Músculos peitorais"))
        costas = grupo_service.criar(GrupoMuscular("Costas", "Músculos dorsais"))

        supino = exercicio_service.criar(
            Exercicio("Supino reto", peito.id, equipamento="Barra")
        )
        remada = exercicio_service.criar(
            Exercicio("Remada curvada", costas.id, equipamento="Barra")
        )

        treino = treino_service.criar(
            Treino(
                nome="Treino de demonstração",
                data=date.today().isoformat(),
                duracao_min=60,
                observacoes="Dados carregados pelo script seed.py"
            )
        )

        serie_service.criar(Serie(treino.id, supino.id, 1, 10, 40))
        serie_service.criar(Serie(treino.id, supino.id, 2, 8, 45))
        serie_service.criar(Serie(treino.id, remada.id, 1, 10, 35))

        print("Dados de exemplo adicionados ao banco treinolog.db.")
    finally:
        db.fechar()


if __name__ == "__main__":
    carregar_dados_exemplo()
