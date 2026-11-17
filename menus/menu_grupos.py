from utils.formatacao import titulo, barra, tabela
import sqlite3
from models.grupo_muscular import GrupoMuscular
from exceptions import RegistroNaoEncontradoError

class MenuGrupos:

    def __init__(self, grupo_service):
        self.grupo_service = grupo_service

    def cadastrar(self) -> None:
        nome = input("Digite o nome do grupo muscular: ")
        descricao = input("Digite a descrição: ")
        grupo = GrupoMuscular(nome, descricao)
        try:
            self.grupo_service.criar(grupo)
        except ValueError:
            print("Houve um erro na criação do grupo, tente novamente.")
        except sqlite3.IntegrityError:
            print("Já existe um grupo muscular com esse nome.")
        else: 
            print("Grupo muscular criado com sucesso!")

    def listar(self) -> None:
        grupos = self.grupo_service.listar()
        if not grupos:
            print("Nenhum grupo muscular cadastrado.")
            return
        cabecalhos = ["ID", "Nome", "Descrição"]
        linhas = []
        for grupo in grupos:
            linhas.append([
                str(grupo.id),
                grupo.nome,
                grupo.descricao or "-"
            ])
        print(tabela(cabecalhos, linhas))

    def buscar(self) -> None:
        try:
            id = int(input("Digite o ID do grupo muscular: "))
            grupo = self.grupo_service.buscar_por_id(id)
        except ValueError as erro:  
            print(f"Entrada inválida: {erro}")
            return
        except RegistroNaoEncontradoError as erro:
            print(erro)
            return
        cabecalhos = ["ID", "Nome", "Descrição"]
        linhas = [[str(grupo.id), grupo.nome, grupo.descricao or "-"]]
        print(tabela(cabecalhos, linhas))

    def atualizar(self) -> None:
        try:
            id = int(input("Digite o ID do grupo que deseja atualizar: "))
            grupo = self.grupo_service.buscar_por_id(id)
            print(f"\nGrupo selecionado: {grupo.nome}")
            nome = input("Digite o novo nome: ")
            descricao = input("Digite a nova descrição: ")
            grupo.nome = nome
            grupo.descricao = descricao
            self.grupo_service.atualizar(grupo)
        except ValueError as erro:
            print(f"Não foi possível atualizar o grupo: {erro}")
        except RegistroNaoEncontradoError as erro:
                print(erro)
        else:
            print("Grupo muscular atualizado com sucesso!")

    def deletar(self) -> None:
        try:
            id = int(input("Digite o ID do grupo que deseja excluir: "))
            grupo = self.grupo_service.buscar_por_id(id)
            print(f"\nGrupo selecionado: {grupo.nome}")
            confirmacao = input("Tem certeza que deseja excluir? (s/n): ").strip().lower()
            if confirmacao != "s":
                print("Exclusão cancelada.")
                return
            self.grupo_service.deletar(id)
        except ValueError as erro:
            print(f"Não foi possível excluir o grupo: {erro}")
        except RegistroNaoEncontradoError as erro:
            print(erro)
        else:
            print("Grupo muscular excluído com sucesso!")

    def exibir(self):
        print(titulo("GERENCIAMENTO DE GRUPOS MUSCULARES"))
        print()
        print("1 - Cadastrar grupo muscular")
        print("2 - Listar grupos musculares")
        print("3 - Buscar grupo muscular")
        print("4 - Atualizar grupo muscular")
        print("5 - Excluir grupo muscular")
        print("6 - Voltar")
        print()
        print(barra())

    def executar(self):
        while True:
            self.exibir()
            try: 
                escolha = int(input("Digite a sua escolha: "))
            except ValueError:
                print("Valor inválido digitado, tente novamente.")
                continue
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
                    print("Opção inválida! Escolha entre 1 e 6")