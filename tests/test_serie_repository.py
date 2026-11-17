import pytest

from database import Database
from models.grupo_muscular import GrupoMuscular
from models.exercicio import Exercicio
from models.treino import Treino
from models.serie import Serie
from repositories.serie_repository import SerieRepository
from exceptions import RegistroNaoEncontradoError


@pytest.fixture
def repository(tmp_path):
    caminho = tmp_path / "teste.db"

    db = Database(str(caminho))
    db.criar_tabelas()

    repo = SerieRepository(db)

    yield repo

    db.fechar()


@pytest.fixture
def dados(repository):
    # Criar grupo muscular
    cursor = repository.db.conexao.execute(
        """
        INSERT INTO grupos_musculares (nome, descricao)
        VALUES (?, ?)
        """,
        ("Peito", "Músculos do peitoral")
    )
    grupo_id = cursor.lastrowid

    # Criar exercício
    cursor = repository.db.conexao.execute(
        """
        INSERT INTO exercicios (nome, grupo_id, equipamento)
        VALUES (?, ?, ?)
        """,
        ("Supino reto", grupo_id, "Barra")
    )
    exercicio_id = cursor.lastrowid

    # Criar treino
    cursor = repository.db.conexao.execute(
        """
        INSERT INTO treinos (nome, data, duracao_min, observacoes)
        VALUES (?, ?, ?, ?)
        """,
        ("Treino A", "2026-11-10", 60, "Treino de peito")
    )
    treino_id = cursor.lastrowid

    repository.db.conexao.commit()

    return {
        "exercicio_id": exercicio_id,
        "treino_id": treino_id
    }


def test_criar_serie(repository, dados):
    serie = Serie(
        treino_id=dados["treino_id"],
        exercicio_id=dados["exercicio_id"],
        numero_serie=1,
        repeticoes=10,
        carga_kg=40
    )

    resultado = repository.criar(serie)

    assert resultado.id is not None
    assert resultado.treino_id == dados["treino_id"]
    assert resultado.exercicio_id == dados["exercicio_id"]
    assert resultado.numero_serie == 1
    assert resultado.repeticoes == 10
    assert resultado.carga_kg == 40


def test_buscar_por_id(repository, dados):
    serie = Serie(
        treino_id=dados["treino_id"],
        exercicio_id=dados["exercicio_id"],
        numero_serie=1,
        repeticoes=10,
        carga_kg=40
    )

    repository.criar(serie)

    resultado = repository.buscar_por_id(serie.id)

    assert resultado.id == serie.id
    assert resultado.exercicio_nome == "Supino reto"
    assert resultado.repeticoes == 10


def test_buscar_por_id_inexistente(repository):
    with pytest.raises(RegistroNaoEncontradoError):
        repository.buscar_por_id(999)


def test_listar_todos(repository, dados):
    repository.criar(
        Serie(dados["treino_id"], dados["exercicio_id"], 1, 10, 40)
    )

    repository.criar(
        Serie(dados["treino_id"], dados["exercicio_id"], 2, 8, 45)
    )

    resultado = repository.listar_todos()

    assert len(resultado) == 2
    assert resultado[0].numero_serie == 1
    assert resultado[1].numero_serie == 2


def test_listar_por_treino(repository, dados):
    repository.criar(
        Serie(dados["treino_id"], dados["exercicio_id"], 1, 10, 40)
    )

    resultado = repository.listar_por_treino(dados["treino_id"])

    assert len(resultado) == 1
    assert resultado[0].treino_id == dados["treino_id"]


def test_listar_por_exercicio(repository, dados):
    repository.criar(
        Serie(dados["treino_id"], dados["exercicio_id"], 1, 10, 40)
    )

    resultado = repository.listar_por_exercicio(dados["exercicio_id"])

    assert len(resultado) == 1
    assert resultado[0].exercicio_id == dados["exercicio_id"]


def test_listar_treino_sem_series(repository, dados):
    resultado = repository.listar_por_treino(dados["treino_id"])

    assert resultado == []


def test_listar_exercicio_sem_series(repository, dados):
    resultado = repository.listar_por_exercicio(dados["exercicio_id"])

    assert resultado == []


def test_atualizar(repository, dados):
    serie = Serie(
        dados["treino_id"],
        dados["exercicio_id"],
        1,
        10,
        40
    )

    repository.criar(serie)

    serie.repeticoes = 12
    serie.carga_kg = 45

    repository.atualizar(serie)

    resultado = repository.buscar_por_id(serie.id)

    assert resultado.repeticoes == 12
    assert resultado.carga_kg == 45


def test_atualizar_id_inexistente(repository, dados):
    serie = Serie(
        treino_id=dados["treino_id"],
        exercicio_id=dados["exercicio_id"],
        numero_serie=1,
        repeticoes=10,
        carga_kg=40,
        id=999
    )

    with pytest.raises(RegistroNaoEncontradoError):
        repository.atualizar(serie)


def test_deletar(repository, dados):
    serie = Serie(
        dados["treino_id"],
        dados["exercicio_id"],
        1,
        10,
        40
    )

    repository.criar(serie)

    repository.deletar(serie.id)

    with pytest.raises(RegistroNaoEncontradoError):
        repository.buscar_por_id(serie.id)


def test_deletar_id_inexistente(repository):
    with pytest.raises(RegistroNaoEncontradoError):
        repository.deletar(999)