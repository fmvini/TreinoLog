from utils.formatacao import titulo, barra, tabela
from models.exercicio import Exercicio
from exceptions import RegistroNaoEncontradoError, RegraDeNegocioError
from utils.entrada import ler_inteiro

class MenuExercicios:
    def __init__(self, exercicio_service, grupo_service):
        self.exercicio_service = exercicio_service
        self.grupo_service = grupo_service

    def cadastrar(self) -> None:
        grupos = self.grupo_service.listar()
        if not grupos:
            print("Não existem grupos musculares cadastrados.")
            print("Cadastre um grupo antes de criar um exercício.")
            return
        print("\nGRUPOS MUSCULARES DISPONÍVEIS")
        cabecalhos = ["ID", "Nome", "Descrição"]
        linhas = []
        for grupo in grupos:
            linhas.append([
                str(grupo.id),
                grupo.nome,
                grupo.descricao or "-"
            ])
        print(tabela(cabecalhos, linhas))
        try:
            nome = input("\nDigite o nome do exercício: ")
            grupo_id = ler_inteiro("Digite o ID do grupo muscular: ")
            equipamento = input("Digite o equipamento (opcional): ")
            exercicio = Exercicio(
                nome=nome,
                grupo_id=grupo_id,
                equipamento=equipamento
            )
            self.exercicio_service.criar(exercicio)
        except ValueError as erro:
            print(f"Não foi possível cadastrar o exercício: {erro}")
        except TypeError as erro:
            print(f"Tipo de dado inválido: {erro}")
        except RegistroNaoEncontradoError as erro:
            print(erro)
        else:
            print("Exercício cadastrado com sucesso!")

    def listar(self) -> None:
        exercicios = self.exercicio_service.listar()
        if not exercicios:
            print("Nenhum exercício cadastrado.")
            return
        cabecalhos = ["ID", "Nome", "Grupo muscular", "Equipamento"]
        linhas = []
        for exercicio in exercicios:
            linhas.append([
                str(exercicio.id),
                exercicio.nome,
                exercicio.grupo_nome or "-",
                exercicio.equipamento or "-"
            ])
        print(tabela(cabecalhos, linhas))

    def buscar(self) -> None:
        try:
            id = ler_inteiro("Digite o ID do exercício: ")
            exercicio = self.exercicio_service.buscar_por_id(id)
        except ValueError as erro:
            print(f"Entrada inválida: {erro}")
            return
        except RegistroNaoEncontradoError as erro:
            print(erro)
            return
        cabecalhos = ["ID", "Nome", "Grupo muscular", "Equipamento"]
        linhas = [[
            str(exercicio.id),
            exercicio.nome,
            exercicio.grupo_nome or "-",
            exercicio.equipamento or "-"
        ]]
        print(tabela(cabecalhos, linhas))

    def atualizar(self) -> None:
        try:
            id = ler_inteiro("Digite o ID do exercício que deseja atualizar: ")
            exercicio = self.exercicio_service.buscar_por_id(id)
            print(f"\nExercício selecionado: {exercicio.nome}")
            grupos = self.grupo_service.listar()
            if not grupos:
                print("Não existem grupos musculares cadastrados.")
                return
            print("\nGRUPOS MUSCULARES DISPONÍVEIS")
            cabecalhos = ["ID", "Nome"]
            linhas = []
            for grupo in grupos:
                linhas.append([str(grupo.id), grupo.nome])
            print(tabela(cabecalhos, linhas))
            nome = input("\nDigite o novo nome: ")
            grupo_id = ler_inteiro("Digite o novo ID do grupo muscular: ")
            equipamento = input("Digite o novo equipamento (opcional): ")
            exercicio.nome = nome
            exercicio.grupo_id = grupo_id
            exercicio.equipamento = equipamento
            self.exercicio_service.atualizar(exercicio)
        except ValueError as erro:
            print(f"Não foi possível atualizar o exercício: {erro}")
        except TypeError as erro:
            print(f"Tipo de dado inválido: {erro}")
        except RegistroNaoEncontradoError as erro:
            print(erro)
        else:
            print("Exercício atualizado com sucesso!")

    def deletar(self) -> None:
        try:
            id = ler_inteiro("Digite o ID do exercício que deseja excluir: ")
            exercicio = self.exercicio_service.buscar_por_id(id)
            print(f"\nExercício selecionado: {exercicio.nome}")
            print(f"Grupo muscular: {exercicio.grupo_nome or '-'}")
            confirmacao = input(
                "\nTem certeza que deseja excluir este exercício? (s/n): "
            ).strip().lower()
            if confirmacao != "s":
                print("Exclusão cancelada.")
                return
            self.exercicio_service.deletar(id)
        except ValueError as erro:
            print(f"Não foi possível excluir o exercício: {erro}")
        except TypeError as erro:
            print(f"Tipo de dado inválido: {erro}")
        except RegistroNaoEncontradoError as erro:
            print(erro)
        except RegraDeNegocioError as erro:
            print(f"Não foi possível excluir o exercício: {erro}")
        else:
            print("Exercício excluído com sucesso!")

    def exibir(self) -> None:
        print(titulo("GERENCIAMENTO DE EXERCÍCIOS"))
        print()
        print("1 - Cadastrar exercício")
        print("2 - Listar exercícios")
        print("3 - Buscar exercício")
        print("4 - Atualizar exercício")
        print("5 - Excluir exercício")
        print("6 - Voltar")
        print()
        print(barra())

    def executar(self) -> None:
        while True:
            self.exibir()

            escolha = ler_inteiro("Digite sua escolha: ")

            match escolha:
                case 1:
                    self.cadastrar()
                case 2:
                    self.listar()
                case 3:
                    self.buscar()
                case 4:
                    self.atualizar()
                case 5:
                    self.deletar()
                case 6:
                    print("Voltando ao menu principal.")
                    break
                case _:
                    print("Opção inválida! Escolha entre 1 e 6.")