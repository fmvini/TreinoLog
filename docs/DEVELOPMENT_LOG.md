## 2026-11-17 — Exclusão em cascata de registros dependentes

### Implementado
- Excluir um exercício remove suas séries vinculadas dentro da mesma transação.
- Excluir um grupo muscular remove seus exercícios e as séries desses exercícios.
- As confirmações de exclusão informam quando registros relacionados também serão removidos.
- Adicionados testes para exclusão de exercício e grupo com registros dependentes.

### Arquivos principais alterados
- `repositories/exercicio_repository.py`
- `repositories/grupo_muscular_repository.py`
- `menus/menu_exercicios.py`
- `menus/menu_grupos.py`
- `menus/menu_treinos.py`
- `tests/test_services.py`
- `docs/DEVELOPMENT_LOG.md`

### Decisões técnicas
- As exclusões de pai e filhos são feitas na mesma transação do repositório, sem depender de alteração/migração do esquema SQLite existente.

### Estado atual
- As exclusões em cascata removem filhos vinculados sem interromper o programa.
- Os 43 testes automatizados passaram, incluindo exclusão de exercício e grupo com registros dependentes.

### Próximos passos
- Continuar o uso normal; as confirmações informam quais registros relacionados também serão excluídos.

## 2026-11-17 — Dados de demonstração e dependência de testes

### Implementado
- Preenchido `seed.py` com dados de exemplo para grupos, exercícios, treino e séries.
- O script cria as tabelas e só carrega exemplos se o banco estiver vazio, preservando qualquer dado existente.
- Adicionado `pytest` a `requirements.txt` como dependência de desenvolvimento e atualizado o README.

### Arquivos principais alterados
- `seed.py`
- `requirements.txt`
- `README.md`
- `docs/DEVELOPMENT_LOG.md`

### Decisões técnicas
- A carga de exemplo usa os services existentes e recusa alterar bancos que já contenham registros.

### Estado atual
- Os arquivos antes vazios agora têm função ou conteúdo útil. Os `__init__.py` vazios foram mantidos como marcadores dos pacotes Python.
- Os testes não foram executados nesta alteração.

### Próximos passos
- Em um banco vazio, executar `python seed.py` para criar dados demonstrativos; instalar `requirements.txt` antes de executar os testes.

## 2026-11-17 — Documentação de uso do TreinoLog

### Implementado
- Criado o README com requisitos, instalação, execução, fluxo de uso, estrutura do projeto e modelo de dados.
- Documentadas as dependências: nenhuma biblioteca externa para executar a aplicação; `pytest` é usado somente para os testes.

### Arquivos principais alterados
- `README.md`
- `docs/DEVELOPMENT_LOG.md`

### Decisões técnicas
- O README exige Python 3.10 ou superior por causa da sintaxe de tipos e dos menus `match/case` usados pelo projeto.

### Estado atual
- A documentação de uso está disponível na raiz do repositório.
- Esta alteração é apenas documental; os testes não foram executados nesta etapa.

### Próximos passos
- Executar `python main.py` na pasta do projeto para iniciar a aplicação.

## 2026-11-17 — Validação de grupos e entradas numéricas

### Implementado
- Confirmada a lógica existente de confirmação: `s` retorna `True`, `n` retorna `False` e entradas inválidas repetem a pergunta.
- Padronizadas as leituras de números nos menus com `ler_inteiro()`.
- Adicionada validação de nomes duplicados de grupos no service, incluindo atualização sem bloquear o próprio registro.
- O menu de grupos agora informa a mensagem clara do service ao falhar o cadastro.

### Arquivos principais alterados
- `menus/menu_grupos.py`
- `menus/menu_exercicios.py`
- `menus/menu_treinos.py`
- `menus/menu_series.py`
- `services/grupo_muscular_service.py`

### Decisões técnicas
- A verificação de duplicidade usa a listagem já existente no repositório e compara nomes conforme a unicidade atual do SQLite.

### Estado atual
- Os 41 testes automatizados existentes passaram.
- Os cinco menus, a confirmação e os casos de duplicidade foram verificados.

### Próximos passos
- Continuar o desenvolvimento normalmente; nenhuma pendência desta alteração.
