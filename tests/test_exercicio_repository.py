
import pytest

from database import Database
from models.grupo_muscular import GrupoMuscular
from models.exercicio import Exercicio
from repositories.exercicio_repository import ExercicioRepository
from exceptions import RegistroNaoEncontradoError


@pytest.fixture
def repository(tmp_path):
    caminho = tmp_path / "teste.db"

    db = Database(str(caminho))
    db.criar_tabelas()

    repo = ExercicioRepository(db)

    yield repo

    db.fechar()


@pytest.fixture
def grupo_id(repository):
    cursor = repository.db.conexao.execute(
        """
        INSERT INTO grupos_musculares (nome, descricao)
        VALUES (?, ?)
        """,
        ("Peito", "Músculos do peitoral")
    )

    repository.db.conexao.commit()

    return cursor.lastrowid


def test_criar_exercicio(repository, grupo_id):
    exercicio = Exercicio(
        nome="Supino reto",
        grupo_id=grupo_id,
        equipamento="Barra"
    )

    resultado = repository.criar(exercicio)

    assert resultado.id is not None
    assert resultado.nome == "Supino reto"
    assert resultado.grupo_id == grupo_id
    assert resultado.equipamento == "Barra"


def test_buscar_por_id(repository, grupo_id):
    exercicio = Exercicio(
        nome="Supino reto",
        grupo_id=grupo_id,
        equipamento="Barra"
    )

    repository.criar(exercicio)

    resultado = repository.buscar_por_id(exercicio.id)

    assert resultado.id == exercicio.id
    assert resultado.nome == "Supino reto"
    assert resultado.grupo_id == grupo_id
    assert resultado.grupo_nome == "Peito"


def test_buscar_por_id_inexistente(repository):
    with pytest.raises(RegistroNaoEncontradoError):
        repository.buscar_por_id(999)


def test_listar_todos(repository, grupo_id):
    repository.criar(
        Exercicio("Supino reto", grupo_id, "Barra")
    )

    repository.criar(
        Exercicio("Crucifixo", grupo_id, "Halteres")
    )

    resultado = repository.listar_todos()

    assert len(resultado) == 2
    assert resultado[0].grupo_nome == "Peito"


def test_listar_por_grupo(repository, grupo_id):
    repository.criar(
        Exercicio("Supino reto", grupo_id, "Barra")
    )

    repository.criar(
        Exercicio("Crucifixo", grupo_id, "Halteres")
    )

    resultado = repository.listar_por_grupo(grupo_id)

    assert len(resultado) == 2

    for exercicio in resultado:
        assert exercicio.grupo_id == grupo_id


def test_listar_grupo_sem_exercicios(repository, grupo_id):
    resultado = repository.listar_por_grupo(grupo_id)

    assert resultado == []


def test_atualizar(repository, grupo_id):
    exercicio = Exercicio(
        nome="Supino reto",
        grupo_id=grupo_id,
        equipamento="Barra"
    )

    repository.criar(exercicio)

    exercicio.nome = "Supino inclinado"
    exercicio.equipamento = "Halteres"

    repository.atualizar(exercicio)

    resultado = repository.buscar_por_id(exercicio.id)

    assert resultado.nome == "Supino inclinado"
    assert resultado.equipamento == "Halteres"


def test_atualizar_id_inexistente(repository, grupo_id):
    exercicio = Exercicio(
        nome="Supino reto",
        grupo_id=grupo_id,
        equipamento="Barra",
        id=999
    )

    with pytest.raises(RegistroNaoEncontradoError):
        repository.atualizar(exercicio)


def test_deletar(repository, grupo_id):
    exercicio = Exercicio(
        nome="Supino reto",
        grupo_id=grupo_id,
        equipamento="Barra"
    )

    repository.criar(exercicio)

    repository.deletar(exercicio.id)

    with pytest.raises(RegistroNaoEncontradoError):
        repository.buscar_por_id(exercicio.id)


def test_deletar_id_inexistente(repository):
    with pytest.raises(RegistroNaoEncontradoError):
        repository.deletar(999)
