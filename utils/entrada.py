from datetime import datetime, date

def ler_inteiro(mensagem: str) -> int:
    while True:
        valor = input(mensagem)
        try:
            valor = int(valor)
            return valor
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")

def ler_decimal(mensagem: str) -> float:
    while True:
        valor = input(mensagem)
        try:
            valor = float(valor)
            return valor
        except ValueError:
            print("Entrada inválida! Digite um número decimal.")

def ler_texto(mensagem: str) -> str:
    while True:
        msg = input(mensagem)
        msg = msg.strip()
        if not msg:
            print("Entrada inválida! O texto não pode ser vazio.")
        else:
            return msg

def ler_data(mensagem: str) -> str:
    while True:
        valor = input(mensagem)
        try:
            datetime.strptime(valor, '%d/%m/%Y')
            return valor
        except ValueError:
            print("Entrada inválida! Digite uma data no formato 'dd/mm/aaaa'.")

def confirmar(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta == "s":
            return True
        if resposta == "n":
            return False
        print("Opção inválida, escolha entre S/N.")