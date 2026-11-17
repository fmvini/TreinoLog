from database import Database

from repositories.grupo_muscular_repository import GrupoMuscularRepository
from repositories.exercicio_repository import ExercicioRepository
from repositories.treino_repository import TreinoRepository
from repositories.serie_repository import SerieRepository

from services.grupo_muscular_service import GrupoMuscularService
from services.exercicio_service import ExercicioService
from services.treino_service import TreinoService
from services.serie_service import SerieService

from menus.menu_principal import MenuPrincipal

def main():
    db = Database()

    try:
        db.criar_tabelas()

        # Repositories
        grupo_repository = GrupoMuscularRepository(db)
        exercicio_repository = ExercicioRepository(db)
        treino_repository = TreinoRepository(db)
        serie_repository = SerieRepository(db)

        # Services
        grupo_service = GrupoMuscularService(grupo_repository)
        exercicio_service = ExercicioService(exercicio_repository, grupo_repository)
        treino_service = TreinoService(treino_repository)
        serie_service = SerieService(serie_repository, treino_repository, exercicio_repository)

                    # Inicialização do menu principal
        menu = MenuPrincipal(
            grupo_service,
            exercicio_service,
            treino_service,
            serie_service
        )

        menu.executar()

        print("TreinoLog inicializado com sucesso!")
    finally:
        db.fechar()

if __name__ == "__main__":
    main()
