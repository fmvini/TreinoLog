from datetime import datetime

def titulo(texto: str) -> str:
    linha = "="*40
    return f"{linha}\n{texto.center(40)}\n{linha}"

def formatar_data_br(data: str) -> str:
    resposta = datetime.strptime(data, '%Y-%m-%d')
    final = datetime.strftime(resposta, '%d/%m/%Y')
    return final

def formatar_carga(carga: int | float) -> str:
    resposta = str(carga).replace(".", ",")
    return f"{resposta} kg"

def formatar_volume(volume: int | float) -> str:
    return formatar_carga(volume)

def barra(caractere: str = "-", tamanho: int = 40) -> str:
    return caractere * tamanho

def tabela(cabecalhos: list[str], linhas: list[list[str]]) -> str:
    if not cabecalhos:
        return ""
    larguras = []
    for indice, cabecalho in enumerate(cabecalhos):
        largura = max(
            [len(cabecalho)] + [len(linha[indice]) for linha in linhas]
        )
        larguras.append(largura)
    borda = "+".join("-" * (largura + 2) for largura in larguras)
    borda = f"+{borda}+"
    def criar_linha(valores: list[str]) -> str:
        celulas = []
        for texto, largura in zip(valores, larguras):
            celulas.append(f" {texto:<{largura}} ")
        return "|" + "|".join(celulas) + "|"
    resultado = []
    resultado.append(borda)
    resultado.append(criar_linha(cabecalhos))
    resultado.append(borda)
    for linha in linhas:
        resultado.append(criar_linha(linha))
    resultado.append(borda)
    return "\n".join(resultado)