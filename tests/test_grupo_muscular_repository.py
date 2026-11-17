
import pytest

from database import Database
from models.grupo_muscular import GrupoMuscular
from repositories.grupo_muscular_repository import GrupoMuscularRepository
from exceptions import RegistroNaoEncontradoError


@pytest.fixture
def repository(tmp_path):
    caminho = tmp_path / "teste.db"

    db = Database(str(caminho))
    db.criar_tabelas()

    repo = GrupoMuscularRepository(db)

    yield repo

    db.fechar()


def test_criar_grupo(repository):
    grupo = GrupoMuscular(nome="Peito", descricao="Músculos do peitoral")

    resultado = repository.criar(grupo)

    assert resultado.id is not None
    assert resultado.nome == "Peito"
    assert resultado.descricao == "Músculos do peitoral"


def test_buscar_por_id(repository):
    grupo = GrupoMuscular(nome="Costas")
    repository.criar(grupo)

    resultado = repository.buscar_por_id(grupo.id)

    assert resultado.id == grupo.id
    assert resultado.nome == "Costas"


def test_buscar_por_id_inexistente(repository):
    with pytest.raises(RegistroNaoEncontradoError):
        repository.buscar_por_id(999)


def test_listar_todos(repository):
    repository.criar(GrupoMuscular(nome="Peito"))
    repository.criar(GrupoMuscular(nome="Costas"))
    repository.criar(GrupoMuscular(nome="Pernas"))

    resultado = repository.listar_todos()

    assert len(resultado) == 3
    assert [grupo.nome for grupo in resultado] == [
        "Costas",
        "Peito",
        "Pernas"
    ]


def test_atualizar(repository):
    grupo = GrupoMuscular(nome="Peito")
    repository.criar(grupo)

    grupo.nome = "Peitoral"
    grupo.descricao = "Músculos do peitoral"

    repository.atualizar(grupo)

    resultado = repository.buscar_por_id(grupo.id)

    assert resultado.nome == "Peitoral"
    assert resultado.descricao == "Músculos do peitoral"


def test_atualizar_id_inexistente(repository):
    grupo = GrupoMuscular(
        nome="Peito",
        id=999
    )

    with pytest.raises(RegistroNaoEncontradoError):
        repository.atualizar(grupo)


def test_deletar(repository):
    grupo = GrupoMuscular(nome="Peito")
    repository.criar(grupo)

    repository.deletar(grupo.id)

    with pytest.raises(RegistroNaoEncontradoError):
        repository.buscar_por_id(grupo.id)


def test_deletar_id_inexistente(repository):
    with pytest.raises(RegistroNaoEncontradoError):
        repository.deletar(999)
