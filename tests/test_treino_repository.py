import pytest

from database import Database
from models.treino import Treino
from repositories.treino_repository import TreinoRepository
from exceptions import RegistroNaoEncontradoError


@pytest.fixture
def repository(tmp_path):
    caminho = tmp_path / "teste.db"

    db = Database(str(caminho))
    db.criar_tabelas()

    repo = TreinoRepository(db)

    yield repo

    db.fechar()


def test_criar_treino(repository):
    treino = Treino(
        nome="Treino A",
        data="2026-11-10",
        duracao_min=60,
        observacoes="Treino de peito"
    )

    resultado = repository.criar(treino)

    assert resultado.id is not None
    assert resultado.nome == "Treino A"
    assert resultado.data == "2026-11-10"
    assert resultado.duracao_min == 60
    assert resultado.observacoes == "Treino de peito"


def test_buscar_por_id(repository):
    treino = Treino(
        nome="Treino A",
        data="2026-11-10",
        duracao_min=60,
        observacoes="Treino de peito"
    )

    repository.criar(treino)

    resultado = repository.buscar_por_id(treino.id)

    assert resultado.id == treino.id
    assert resultado.nome == "Treino A"
    assert resultado.data == "2026-11-10"


def test_buscar_por_id_inexistente(repository):
    with pytest.raises(RegistroNaoEncontradoError):
        repository.buscar_por_id(999)


def test_listar_todos(repository):
    repository.criar(
        Treino("Treino A", "2026-11-10", 60, "Peito")
    )

    repository.criar(
        Treino("Treino B", "2026-11-12", 45, "Costas")
    )

    resultado = repository.listar_todos()

    assert len(resultado) == 2
    assert {treino.nome for treino in resultado} == {"Treino A", "Treino B"}


def test_listar_por_periodo(repository):
    repository.criar(
        Treino("Treino A", "2026-11-05", 60, "Peito")
    )

    repository.criar(
        Treino("Treino B", "2026-11-10", 45, "Costas")
    )

    repository.criar(
        Treino("Treino C", "2026-11-12", 50, "Pernas")
    )

    resultado = repository.listar_por_periodo(
        "2026-11-09",
        "2026-11-13"
    )

    assert len(resultado) == 2
    assert {treino.nome for treino in resultado} == {"Treino B", "Treino C"}


def test_listar_periodo_sem_resultados(repository):
    resultado = repository.listar_por_periodo(
        "2026-11-10",
        "2026-11-15"
    )

    assert resultado == []


def test_atualizar(repository):
    treino = Treino(
        nome="Treino A",
        data="2026-11-10",
        duracao_min=60,
        observacoes="Peito"
    )

    repository.criar(treino)

    treino.nome = "Treino B"
    treino.duracao_min = 75
    treino.observacoes = "Peito e tríceps"

    repository.atualizar(treino)

    resultado = repository.buscar_por_id(treino.id)

    assert resultado.nome == "Treino B"
    assert resultado.duracao_min == 75
    assert resultado.observacoes == "Peito e tríceps"


def test_atualizar_id_inexistente(repository):
    treino = Treino(
        nome="Treino A",
        data="2026-11-10",
        duracao_min=60,
        id=999
    )

    with pytest.raises(RegistroNaoEncontradoError):
        repository.atualizar(treino)


def test_deletar(repository):
    treino = Treino(
        nome="Treino A",
        data="2026-11-10",
        duracao_min=60
    )

    repository.criar(treino)

    repository.deletar(treino.id)

    with pytest.raises(RegistroNaoEncontradoError):
        repository.buscar_por_id(treino.id)


def test_deletar_id_inexistente(repository):
    with pytest.raises(RegistroNaoEncontradoError):
        repository.deletar(999)