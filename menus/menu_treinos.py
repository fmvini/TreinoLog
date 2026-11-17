from utils.formatacao import titulo, barra, tabela
from utils.formatacao import formatar_data_br
from models.treino import Treino
from exceptions import RegistroNaoEncontradoError
from utils.entrada import ler_inteiro


class MenuTreinos:

    def __init__(self, treino_service):
        self.treino_service = treino_service

    def cadastrar(self) -> None:
        try:
            nome = input("Digite o nome do treino: ")
            data = input("Digite a data do treino (AAAA-MM-DD): ")
            duracao_min = ler_inteiro("Digite a duração em minutos: ")
            observacoes = input("Digite as observações (opcional): ")
            treino = Treino(
                nome=nome,
                data=data,
                duracao_min=duracao_min,
                observacoes=observacoes
            )
            self.treino_service.criar(treino)
        except ValueError as erro:
            print(f"Não foi possível cadastrar o treino: {erro}")
        except TypeError as erro:
            print(f"Tipo de dado inválido: {erro}")
        else:
            print("Treino cadastrado com sucesso!")

    def listar(self) -> None:
        treinos = self.treino_service.listar()
        if not treinos:
            print("Nenhum treino cadastrado.")
            return
        cabecalhos = ["ID", "Nome", "Data", "Duração (min)", "Observações"]
        linhas = []
        for treino in treinos:
            linhas.append([
                str(treino.id),
                treino.nome,
                treino.data_br,
                str(treino.duracao_min),
                treino.observacoes or "-"
            ])
        print(tabela(cabecalhos, linhas))

    def buscar(self) -> None:
        try:
            id = ler_inteiro("Digite o ID do treino: ")
            treino = self.treino_service.buscar_por_id(id)
        except ValueError as erro:
            print(f"Entrada inválida: {erro}")
            return
        except RegistroNaoEncontradoError as erro:
            print(erro)
            return
        cabecalhos = ["ID", "Nome", "Data", "Duração (min)", "Observações"]
        linhas = [[
            str(treino.id),
            treino.nome,
            treino.data_br,
            str(treino.duracao_min),
            treino.observacoes or "-"
        ]]
        print(tabela(cabecalhos, linhas))

    def atualizar(self) -> None:
        try:
            id = ler_inteiro("Digite o ID do treino que deseja atualizar: ")
            treino = self.treino_service.buscar_por_id(id)
            print(f"\nTreino selecionado: {treino.nome}")
            nome = input("Digite o novo nome: ")
            data = input("Digite a nova data (AAAA-MM-DD): ")
            duracao_min = ler_inteiro("Digite a nova duração em minutos: ")
            observacoes = input("Digite as novas observações (opcional): ")
            treino.nome = nome
            treino.data = data
            treino.duracao_min = duracao_min
            treino.observacoes = observacoes
            self.treino_service.atualizar(treino)
        except ValueError as erro:
            print(f"Não foi possível atualizar o treino: {erro}")
        except TypeError as erro:
            print(f"Tipo de dado inválido: {erro}")
        except RegistroNaoEncontradoError as erro:
            print(erro)
        else:
            print("Treino atualizado com sucesso!")
    def deletar(self) -> None:
        try:
            id = ler_inteiro("Digite o ID do treino que deseja excluir: ")
            treino = self.treino_service.buscar_por_id(id)
            print(f"\nTreino selecionado: {treino.nome}")
            print(f"Data: {treino.data_br}")
            confirmacao = input(
                "\nTem certeza que deseja excluir este treino? (s/n): "
            ).strip().lower()
            if confirmacao != "s":
                print("Exclusão cancelada.")
                return
            self.treino_service.deletar(id)
        except ValueError as erro:
            print(f"Não foi possível excluir o treino: {erro}")
        except TypeError as erro:
            print(f"Tipo de dado inválido: {erro}")
        except RegistroNaoEncontradoError as erro:
            print(erro)
        else:
            print("Treino excluído com sucesso!")

    def exibir(self) -> None:
        print(titulo("GERENCIAMENTO DE TREINOS"))
        print()
        print("1 - Cadastrar treino")
        print("2 - Listar treinos")
        print("3 - Buscar treino")
        print("4 - Atualizar treino")
        print("5 - Excluir treino")
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