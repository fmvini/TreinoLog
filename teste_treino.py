from models.exercicio import Exercicio


# Teste 1: criação de exercício válido
exercicio = Exercicio(
    nome="Supino reto",
    grupo_id=1,
    equipamento="Barra",
    id=3,
    grupo_nome="Peito"
)

assert exercicio.nome == "Supino reto"
assert exercicio.grupo_id == 1
assert exercicio.equipamento == "Barra"

print("[OK] Criação de exercício")


# Teste 2: nome vazio
try:
    Exercicio(nome="   ", grupo_id=1)
    assert False, "Deveria ter lançado ValueError."
except ValueError:
    print("[OK] Validação de nome vazio")


# Teste 3: nome muito longo
try:
    Exercicio(nome="A" * 61, grupo_id=1)
    assert False, "Deveria ter lançado ValueError."
except ValueError:
    print("[OK] Validação de nome muito longo")


# Teste 4: grupo_id inválido
for valor in [0, -1]:
    try:
        Exercicio(nome="Supino", grupo_id=valor)
        assert False, "Deveria ter lançado ValueError."
    except ValueError:
        pass

print("[OK] Validação de grupo_id negativo ou zero")


# Teste 5: grupo_id não inteiro
for valor in [1.5, "1", True]:
    try:
        Exercicio(nome="Supino", grupo_id=valor)
        assert False, "Deveria ter lançado TypeError."
    except TypeError:
        pass

print("[OK] Validação de grupo_id não inteiro")


# Teste 6: equipamento opcional
exercicio_sem_equipamento = Exercicio(
    nome="Flexão",
    grupo_id=1,
    equipamento="   "
)

assert exercicio_sem_equipamento.equipamento is None

print("[OK] Equipamento opcional")


# Teste 7: representação em texto
assert str(exercicio) == "[3] Supino reto (Barra) - Peito"

print("[OK] Método __str__")


print("\nTodos os testes de Exercicio passaram!")