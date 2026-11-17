from utils.formatacao import titulo, barra
from menus.menu_grupos import MenuGrupos
from menus.menu_exercicios import MenuExercicios
from menus.menu_treinos import MenuTreinos
from menus.menu_series import MenuSeries

class MenuPrincipal:
    def __init__(
        self,
        grupo_service,
        exercicio_service,
        treino_service,
        serie_service
    ):
        self.grupo_service = grupo_service
        self.exercicio_service = exercicio_service
        self.treino_service = treino_service
        self.serie_service = serie_service
        self.menu_grupos = MenuGrupos(grupo_service)
        self.menu_exercicios = MenuExercicios(exercicio_service, grupo_service)
        self.menu_treinos = MenuTreinos(treino_service)
        self.menu_series = MenuSeries(serie_service, treino_service, exercicio_service)

    def exibir(self) -> None:
        print(titulo("TREINOLOG"))
        print()
        print("1 - Gerenciar grupos musculares")
        print("2 - Gerenciar exercícios")
        print("3 - Gerenciar treinos")
        print("4 - Gerenciar séries")
        print()
        print("0 - Sair")
        print(barra())

    def executar(self) -> None:
        while True:
            self.exibir()
            try:
                escolha = int(input("Digite sua escolha: "))
            except ValueError:
                print("Valor inválido, digite um valor inteiro.")
                continue
            match escolha:
                case 1:
                    self.menu_grupos.executar()                    
                case 2:
                    self.menu_exercicios.executar()
                case 3:
                    self.menu_treinos.executar()
                case 4:
                    self.menu_series.executar()
                case 0:
                    print("Finalizando serviço.")
                    break
                case _:
                    print("Escolha inválida! escolha entre os valores representados na tabela!")

