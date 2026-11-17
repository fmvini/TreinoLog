from datetime import date

import pytest

from database import Database
from exceptions import RegistroNaoEncontradoError
from models.grupo_muscular import GrupoMuscular
from models.exercicio import Exercicio
from models.treino import Treino
from models.serie import Serie
from repositories.grupo_muscular_repository import GrupoMuscularRepository
from repositories.exercicio_repository import ExercicioRepository
from repositories.treino_repository import TreinoRepository
from repositories.serie_repository import SerieRepository
from services.grupo_muscular_service import GrupoMuscularService
from services.exercicio_service import ExercicioService
from services.treino_service import TreinoService
from services.serie_service import SerieService
from menus.menu_exercicios import MenuExercicios


@pytest.fixture
def sistema(tmp_path):
    db = Database(str(tmp_path / "teste_treinolog.db"))
    db.criar_tabelas()

    grupo_repo = GrupoMuscularRepository(db)
    exercicio_repo = ExercicioRepository(db)
    treino_repo = TreinoRepository(db)
    serie_repo = SerieRepository(db)

    services = {
        "grupo": GrupoMuscularService(grupo_repo),
        "exercicio": ExercicioService(exercicio_repo, grupo_repo),
        "treino": TreinoService(treino_repo),
        "serie": SerieService(serie_repo, treino_repo, exercicio_repo),
    }

    yield services
    db.fechar()


def test_crud_completo_dos_quatro_services(sistema):
    grupo_service = sistema["grupo"]
    exercicio_service = sistema["exercicio"]
    treino_service = sistema["treino"]
    serie_service = sistema["serie"]

    # GRUPO MUSCULAR: criar, atualizar e consultar
    grupo = grupo_service.criar(GrupoMuscular("Peito", "Músculos peitorais"))
    assert grupo.id is not None
    grupo.nome = "Peitoral"
    grupo_service.atualizar(grupo)
    assert grupo_service.repository.buscar_por_id(grupo.id).nome == "Peitoral"

    # EXERCÍCIO: criar, atualizar e consultar
    exercicio = exercicio_service.criar(
        Exercicio("Supino reto", grupo.id, equipamento="Barra")
    )
    assert exercicio.id is not None
    exercicio.nome = "Supino reto com barra"
    exercicio_service.atualizar(exercicio)
    assert exercicio_service.repository.buscar_por_id(exercicio.id).nome == "Supino reto com barra"

    # TREINO: criar, atualizar e consultar
    treino = treino_service.criar(
        Treino("Treino A", date.today().isoformat(), 60, "Treino de peito")
    )
    assert treino.id is not None
    treino.nome = "Treino de peito"
    treino_service.atualizar(treino)
    assert treino_service.repository.buscar_por_id(treino.id).nome == "Treino de peito"

    # SÉRIE: criar, atualizar e consultar
    serie = serie_service.criar(Serie(treino.id, exercicio.id, 1, 10, 40))
    assert serie.id is not None
    serie.repeticoes = 12
    serie.carga_kg = 42.5
    serie_service.atualizar(serie)
    serie_salva = serie_service.serie_repository.buscar_por_id(serie.id)
    assert serie_salva.repeticoes == 12
    assert serie_salva.carga_kg == 42.5

    # Excluir na ordem correta por causa das chaves estrangeiras
    serie_service.deletar(serie.id)
    exercicio_service.deletar(exercicio.id)
    grupo_service.deletar(grupo.id)
    treino_service.deletar(treino.id)

    with pytest.raises(RegistroNaoEncontradoError):
        serie_service.serie_repository.buscar_por_id(serie.id)
    with pytest.raises(RegistroNaoEncontradoError):
        exercicio_service.repository.buscar_por_id(exercicio.id)
    with pytest.raises(RegistroNaoEncontradoError):
        grupo_service.repository.buscar_por_id(grupo.id)
    with pytest.raises(RegistroNaoEncontradoError):
        treino_service.repository.buscar_por_id(treino.id)


def test_excluir_exercicio_com_serie_remove_exercicio_e_serie(
    sistema,
    monkeypatch,
    capsys
):
    grupo = sistema["grupo"].criar(GrupoMuscular("Peito"))
    exercicio = sistema["exercicio"].criar(Exercicio("Supino reto", grupo.id))
    treino = sistema["treino"].criar(
        Treino("Treino A", date.today().isoformat(), 60)
    )
    serie = sistema["serie"].criar(Serie(treino.id, exercicio.id, 1, 10, 40))
    respostas = iter([str(exercicio.id), "s"])
    monkeypatch.setattr("builtins.input", lambda _: next(respostas))

    menu = MenuExercicios(sistema["exercicio"], sistema["grupo"])
    menu.deletar()

    assert "Exercício excluído com sucesso!" in capsys.readouterr().out
    with pytest.raises(RegistroNaoEncontradoError):
        sistema["exercicio"].buscar_por_id(exercicio.id)
    with pytest.raises(RegistroNaoEncontradoError):
        sistema["serie"].buscar_por_id(serie.id)


def test_excluir_grupo_remove_exercicios_e_series_vinculados(sistema):
    grupo = sistema["grupo"].criar(GrupoMuscular("Peito"))
    exercicio = sistema["exercicio"].criar(Exercicio("Supino reto", grupo.id))
    treino = sistema["treino"].criar(
        Treino("Treino A", date.today().isoformat(), 60)
    )
    serie = sistema["serie"].criar(Serie(treino.id, exercicio.id, 1, 10, 40))

    sistema["grupo"].deletar(grupo.id)

    with pytest.raises(RegistroNaoEncontradoError):
        sistema["grupo"].buscar_por_id(grupo.id)
    with pytest.raises(RegistroNaoEncontradoError):
        sistema["exercicio"].buscar_por_id(exercicio.id)
    with pytest.raises(RegistroNaoEncontradoError):
        sistema["serie"].buscar_por_id(serie.id)