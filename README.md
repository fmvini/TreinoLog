# TreinoLog

Aplicação de terminal para registrar treinos de academia. O TreinoLog usa Python e SQLite para gerenciar grupos musculares, exercícios, treinos e séries.

## Funcionalidades

- Cadastro, consulta, atualização e exclusão de grupos musculares.
- Cadastro, consulta, atualização e exclusão de exercícios vinculados a grupos musculares.
- Cadastro, consulta, atualização e exclusão de treinos.
- Registro de séries associadas a um treino e a um exercício.
- Exibição do volume da série (carga × repetições) e de uma estimativa de 1RM.

## Requisitos

- Python 3.10 ou superior.
- SQLite 3, acessado pelo módulo `sqlite3` que acompanha a biblioteca padrão do Python.

A aplicação não depende de bibliotecas externas para funcionar: o acesso ao SQLite usa o módulo `sqlite3` da biblioteca padrão do Python. O arquivo `requirements.txt` contém `pytest`, usado somente para executar os testes.

## Instalação e execução

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/fmvini/TreinoLog.git
cd TreinoLog
```

Opcionalmente, crie e ative um ambiente virtual.

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No macOS ou Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Inicie a aplicação na pasta do projeto:

```bash
python main.py
```

O banco `treinolog.db` e as tabelas são criados automaticamente na primeira execução. O arquivo do banco fica na pasta de onde o comando foi iniciado.

Para carregar dados de demonstração em um banco vazio, execute:

```bash
python seed.py
```

O script adiciona grupos musculares, exercícios, um treino e algumas séries. Se encontrar qualquer registro no banco, não altera os dados existentes.

## Como usar

No menu principal, escolha uma área para gerenciar:

1. Grupos musculares
2. Exercícios
3. Treinos
4. Séries
0. Sair

Cada área oferece opções para cadastrar, listar, buscar, atualizar e excluir registros. Para começar, cadastre um grupo muscular; depois, crie um exercício associado a ele, cadastre um treino e adicione séries vinculando o treino aos exercícios. Use a opção de voltar nos submenus para retornar ao menu principal.

## Banco de dados

O SQLite contém quatro tabelas relacionais:

- `grupos_musculares`: nome e descrição dos grupos.
- `exercicios`: exercícios associados a um grupo muscular.
- `treinos`: nome, data, duração e observações.
- `series`: número, repetições e carga de cada exercício em um treino.

As relações usam chaves estrangeiras: cada exercício pertence a um grupo muscular; cada série pertence a um treino e referencia um exercício.

## Estrutura do projeto

```text
TreinoLog/
├── main.py                  # Inicialização e composição da aplicação
├── seed.py                  # Carga opcional de dados de demonstração
├── database.py              # Conexão SQLite e criação das tabelas
├── models/                  # Modelos de dados e validações
├── repositories/            # Operações SQL de persistência
├── services/                # Regras de negócio
├── menus/                   # Interface de terminal
├── utils/                   # Entrada e formatação
├── tests/                   # Testes automatizados
└── requirements.txt         # Dependência de desenvolvimento: pytest
```

## Testes

Os testes usam `pytest`, que é uma dependência de desenvolvimento. Instale-a pelo arquivo de dependências e execute a suíte assim:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```
