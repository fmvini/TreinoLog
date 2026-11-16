import sqlite3

class Database:
    def __init__(self, caminho: str = 'treinolog.db'):
        self.caminho = caminho
        self._conexao = None

    def conectar(self) -> sqlite3.Connection:
        if self._conexao is None:
            self._conexao = sqlite3.connect(self.caminho)
            self._conexao.row_factory = sqlite3.Row
            self._conexao.execute("PRAGMA foreign_keys = ON")
        return self._conexao
    @property 
    def conexao(self) -> sqlite3.Connection:
        return self.conectar()
    
    def criar_tabelas(self) -> None:
        self.conexao.executescript("""
            CREATE TABLE IF NOT EXISTS grupos_musculares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT
            );

            CREATE TABLE IF NOT EXISTS exercicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                equipamento TEXT,
                grupo_id INTEGER NOT NULL,
                FOREIGN KEY (grupo_id) REFERENCES grupos_musculares(id) ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS treinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data TEXT NOT NULL,
                duracao_min INTEGER CHECK (duracao_min IS NULL OR duracao_min > 0),
                observacoes TEXT
            );

            CREATE TABLE IF NOT EXISTS series (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                treino_id INTEGER NOT NULL,
                exercicio_id INTEGER NOT NULL,
                numero_serie INTEGER NOT NULL CHECK (numero_serie > 0),
                repeticoes INTEGER NOT NULL CHECK (repeticoes > 0),
                carga_kg REAL NOT NULL CHECK (carga_kg >= 0),
                FOREIGN KEY (treino_id) REFERENCES treinos(id) ON DELETE CASCADE,
                FOREIGN KEY (exercicio_id) REFERENCES exercicios(id) ON DELETE RESTRICT
            );
        """)

        self.conexao.commit()

    def fechar(self) -> None:
        if self._conexao is not None:
            self._conexao.close()
            self._conexao = None