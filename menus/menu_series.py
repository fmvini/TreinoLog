from utils.formatacao import titulo, barra, tabela
from models.serie import Serie
from exceptions import RegistroNaoEncontradoError


class MenuSeries:

    def __init__(
        self,
        serie_service,
        treino_service,
        exercicio_service
    ):
        self.serie_service = serie_service
        self.treino_service = treino_service
        self.exercicio_service = exercicio_service

    def cadastrar(self) -> None:
        treinos = self.treino_service.listar()
        exercicios = self.exercicio_service.listar()
        if not treinos:
            print("Nenhum treino cadastrado. Cadastre um treino primeiro.")
            return
        if not exercicios:
            print("Nenhum exercício cadastrado. Cadastre um exercício primeiro.")
            return
        print("\nTREINOS DISPONÍVEIS")
        cabecalhos = ["ID", "Nome", "Data"]
        linhas = []
        for treino in treinos:
            linhas.append([
                str(treino.id),
                treino.nome,
                treino.data_br
            ])
        print(tabela(cabecalhos, linhas))
        print("\nEXERCÍCIOS DISPONÍVEIS")
        cabecalhos = ["ID", "Nome", "Grupo muscular"]
        linhas = []
        for exercicio in exercicios:
            linhas.append([
                str(exercicio.id),
                exercicio.nome,
                exercicio.grupo_nome or "-"
            ])
        print(tabela(cabecalhos, linhas))
        try:
            treino_id = int(input("\nDigite o ID do treino: "))
            exercicio_id = int(input("Digite o ID do exercício: "))
            numero_serie = int(input("Digite o número da série: "))
            repeticoes = int(input("Digite a quantidade de repetições: "))
            carga_kg = float(input("Digite a carga utilizada (kg): "))
            serie = Serie(
                treino_id=treino_id,
                exercicio_id=exercicio_id,
                numero_serie=numero_serie,
                repeticoes=repeticoes,
                carga_kg=carga_kg
            )
            self.serie_service.criar(serie)
        except ValueError as erro:
            print(f"Não foi possível cadastrar a série: {erro}")
        except TypeError as erro:
            print(f"Tipo de dado inválido: {erro}")
        except RegistroNaoEncontradoError as erro:
            print(erro)
        else:
            print("Série cadastrada com sucesso!")

    def listar(self) -> None:
        series = self.serie_service.listar()
        if not series:
            print("Nenhuma série cadastrada.")
            return
        cabecalhos = [
            "ID",
            "Treino",
            "Exercício",
            "Série",
            "Repetições",
            "Carga (kg)",
            "Volume",
            "1RM estimado"
        ]
        linhas = []
        for serie in series:
            linhas.append([
                str(serie.id),
                str(serie.treino_id),
                serie.exercicio_nome or "-",
                str(serie.numero_serie),
                str(serie.repeticoes),
                str(serie.carga_kg).replace(".", ","),
                str(serie.volume).replace(".", ","),
                f"{serie.rm_estimado:.2f}".replace(".", ",")
            ])
        print(tabela(cabecalhos, linhas))

    def buscar(self) -> None:
        try:
            id = int(input("Digite o ID da série: "))
            serie = self.serie_service.buscar_por_id(id)
        except ValueError as erro:
            print(f"Entrada inválida: {erro}")
            return
        except RegistroNaoEncontradoError as erro:
            print(erro)
            return
        cabecalhos = [
            "ID",
            "Treino",
            "Exercício",
            "Série",
            "Repetições",
            "Carga (kg)",
            "Volume",
            "1RM estimado"
        ]
        linhas = [[
            str(serie.id),
            str(serie.treino_id),
            serie.exercicio_nome or "-",
            str(serie.numero_serie),
            str(serie.repeticoes),
            str(serie.carga_kg).replace(".", ","),
            str(serie.volume).replace(".", ","),
            f"{serie.rm_estimado:.2f}".replace(".", ",")
        ]]
        print(tabela(cabecalhos, linhas))

    def atualizar(self) -> None:
        try:
            id = int(input("Digite o ID da série que deseja atualizar: "))
            serie = self.serie_service.buscar_por_id(id)
            print(f"\nSérie selecionada: {serie}")
            print(f"Treino atual: {serie.treino_id}")
            treinos = self.treino_service.listar()
            exercicios = self.exercicio_service.listar()
            if not treinos:
                print("Nenhum treino cadastrado.")
                return
            if not exercicios:
                print("Nenhum exercício cadastrado.")
                return
            print("\nTREINOS DISPONÍVEIS")
            cabecalhos = ["ID", "Nome", "Data"]
            linhas = []
            for treino in treinos:
                linhas.append([
                    str(treino.id),
                    treino.nome,
                    treino.data_br
                ])
            print(tabela(cabecalhos, linhas))
            print("\nEXERCÍCIOS DISPONÍVEIS")
            cabecalhos = ["ID", "Nome", "Grupo muscular"]
            linhas = []
            for exercicio in exercicios:
                linhas.append([
                    str(exercicio.id),
                    exercicio.nome,
                    exercicio.grupo_nome or "-"
                ])
            print(tabela(cabecalhos, linhas))
            treino_id = int(input("\nDigite o novo ID do treino: "))
            exercicio_id = int(input("Digite o novo ID do exercício: "))
            numero_serie = int(input("Digite o novo número da série: "))
            repeticoes = int(input("Digite a nova quantidade de repetições: "))
            carga_kg = float(input("Digite a nova carga (kg): "))
            serie.treino_id = treino_id
            serie.exercicio_id = exercicio_id
            serie.numero_serie = numero_serie
            serie.repeticoes = repeticoes
            serie.carga_kg = carga_kg
            self.serie_service.atualizar(serie)
        except ValueError as erro:
            print(f"Não foi possível atualizar a série: {erro}")
        except TypeError as erro:
            print(f"Tipo de dado inválido: {erro}")
        except RegistroNaoEncontradoError as erro:
            print(erro)
        else:
            print("Série atualizada com sucesso!")

    def deletar(self) -> None:
        try:
            id = int(input("Digite o ID da série que deseja excluir: "))
            serie = self.serie_service.buscar_por_id(id)
            print(f"\nSérie selecionada: {serie}")
            confirmacao = input(
                "\nTem certeza que deseja excluir esta série? (s/n): "
            ).strip().lower()
            if confirmacao != "s":
                print("Exclusão cancelada.")
                return
            self.serie_service.deletar(id)
        except ValueError as erro:
            print(f"Não foi possível excluir a série: {erro}")
        except TypeError as erro:
            print(f"Tipo de dado inválido: {erro}")
        except RegistroNaoEncontradoError as erro:
            print(erro)
        else:
            print("Série excluída com sucesso!")

    def exibir(self) -> None:
        print(titulo("GERENCIAMENTO DE SÉRIES"))
        print()
        print("1 - Cadastrar série")
        print("2 - Listar séries")
        print("3 - Buscar série")
        print("4 - Atualizar série")
        print("5 - Excluir série")
        print("6 - Voltar")
        print()
        print(barra())

    def executar(self) -> None:
        while True:
            self.exibir()

            try:
                escolha = int(input("Digite sua escolha: "))
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
                    print("Opção inválida! Escolha entre 1 e 6.")