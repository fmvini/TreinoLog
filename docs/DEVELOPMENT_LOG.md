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
