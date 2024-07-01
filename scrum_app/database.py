import sqlite3
from datetime import datetime

class GerenciadorBancoDeDados:
    def __init__(self, nome_banco="tarefas.db"):
        """
        Inicializa uma nova conexão com o banco de dados SQLite.
        Se o banco de dados não existir, ele será criado.

        :param nome_banco: Nome do arquivo do banco de dados SQLite.
        """
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        """
        Cria as tabelas necessárias no banco de dados, se elas não existirem.
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas_dia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tarefa TEXT NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL,
            concluida INTEGER DEFAULT 0  -- Adicionando a coluna de status de conclusão
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tarefa TEXT NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            prazo INTEGER NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS colaboradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
        """)

        self.conexao.commit()

    def adicionar_tarefa_dia(self, nome, tarefa, tipo, quantidade):
        """
        Adiciona uma nova tarefa do dia no banco de dados.

        :param nome: Nome do colaborador.
        :param tarefa: Descrição da tarefa.
        :param tipo: Tipo da tarefa (quantidade ou tempo).
        :param quantidade: Quantidade associada à tarefa.
        """
        data = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("""
        INSERT INTO tarefas_dia (nome, tarefa, tipo, quantidade, data, concluida)
        VALUES (?, ?, ?, ?, ?, 0)
        """, (nome, tarefa, tipo, quantidade, data))
        self.conexao.commit()

    def adicionar_tarefa_config(self, nome, tarefa, tipo, quantidade, prazo):
        """
        Adiciona uma nova tarefa de configuração no banco de dados.

        :param nome: Nome da tarefa.
        :param tarefa: Descrição da tarefa.
        :param tipo: Tipo da tarefa (quantidade ou tempo).
        :param quantidade: Quantidade associada à tarefa.
        :param prazo: Prazo em dias para conclusão da tarefa.
        """
        self.cursor.execute("""
        INSERT INTO tarefas_config (nome, tarefa, tipo, quantidade, prazo)
        VALUES (?, ?, ?, ?, ?)
        """, (nome, tarefa, tipo, quantidade, prazo))
        self.conexao.commit()

    def adicionar_colaborador(self, nome):
        """
        Adiciona um novo colaborador no banco de dados.

        :param nome: Nome completo do colaborador.
        """
        self.cursor.execute("""
        INSERT INTO colaboradores (nome)
        VALUES (?)
        """, (nome,))
        self.conexao.commit()

    def buscar_tarefas_dia(self):
        """
        Busca todas as tarefas do dia no banco de dados.

        :return: Lista de todas as tarefas do dia.
        """
        self.cursor.execute("""
        SELECT * FROM tarefas_dia
        """)
        return self.cursor.fetchall()

    def buscar_tarefas_config(self):
        """
        Busca todas as tarefas de configuração no banco de dados.

        :return: Lista de todas as tarefas de configuração.
        """
        self.cursor.execute("""
        SELECT * FROM tarefas_config
        """)
        return self.cursor.fetchall()

    def buscar_tarefas_dia_por_nome(self, nome_tarefa):
        """
        Busca todas as tarefas do dia por nome no banco de dados.

        :param nome_tarefa: Nome da tarefa a ser buscada.
        :return: Lista de todas as tarefas do dia correspondentes ao nome.
        """
        self.cursor.execute("""
        SELECT * FROM tarefas_dia WHERE tarefa=?
        """, (nome_tarefa,))
        return self.cursor.fetchall()

    def buscar_colaboradores(self):
        """
        Busca todos os colaboradores no banco de dados.

        :return: Lista de todos os colaboradores.
        """
        self.cursor.execute("""
        SELECT * FROM colaboradores
        """)
        return self.cursor.fetchall()

    def buscar_tarefa_por_id(self, tabela, id_tarefa):
        """
        Busca uma tarefa por ID no banco de dados.

        :param tabela: Nome da tabela a ser buscada.
        :param id_tarefa: ID da tarefa a ser buscada.
        :return: Tarefa correspondente ao ID.
        """
        self.cursor.execute(f"""
        SELECT * FROM {tabela} WHERE id=?
        """, (id_tarefa,))
        return self.cursor.fetchone()

    def buscar_colaborador_por_id(self, id_colaborador):
        """
        Busca um colaborador por ID no banco de dados.

        :param id_colaborador: ID do colaborador a ser buscado.
        :return: Colaborador correspondente ao ID.
        """
        self.cursor.execute("""
        SELECT * FROM colaboradores WHERE id=?
        """, (id_colaborador,))
        return self.cursor.fetchone()

    def verificar_colaborador_existente(self, nome):
        """
        Verifica se um colaborador já existe no banco de dados.

        :param nome: Nome do colaborador a ser verificado.
        :return: True se o colaborador existe, False caso contrário.
        """
        self.cursor.execute("""
        SELECT * FROM colaboradores WHERE nome=?
        """, (nome,))
        return self.cursor.fetchone() is not None

    def atualizar_tarefa(self, tabela, id_tarefa, nome, tarefa, tipo, quantidade, prazo=None):
        """
        Atualiza uma tarefa no banco de dados.

        :param tabela: Nome da tabela a ser atualizada.
        :param id_tarefa: ID da tarefa a ser atualizada.
        :param nome: Novo nome da tarefa.
        :param tarefa: Nova descrição da tarefa.
        :param tipo: Novo tipo da tarefa.
        :param quantidade: Nova quantidade associada à tarefa.
        :param prazo: Novo prazo em dias para conclusão da tarefa (opcional).
        """
        if tabela == 'tarefas_config':
            self.cursor.execute("""
            UPDATE tarefas_config
            SET nome=?, tarefa=?, tipo=?, quantidade=?, prazo=?
            WHERE id=?
            """, (nome, tarefa, tipo, quantidade, prazo, id_tarefa))
        else:
            self.cursor.execute("""
            UPDATE tarefas_dia
            SET nome=?, tarefa=?, tipo=?, quantidade=?
            WHERE id=?
            """, (nome, tarefa, tipo, quantidade, id_tarefa))
        self.conexao.commit()

    def atualizar_status_tarefa(self, id_tarefa, concluida):
        """
        Atualiza o status de conclusão de uma tarefa.

        :param id_tarefa: ID da tarefa a ser atualizada.
        :param concluida: Novo status de conclusão (0 ou 1).
        """
        self.cursor.execute("""
        UPDATE tarefas_dia
        SET concluida=?
        WHERE id=?
        """, (concluida, id_tarefa))
        self.conexao.commit()

    def atualizar_colaborador(self, id_colaborador, nome):
        """
        Atualiza um colaborador no banco de dados.

        :param id_colaborador: ID do colaborador a ser atualizado.
        :param nome: Novo nome do colaborador.
        """
        self.cursor.execute("""
        UPDATE colaboradores
        SET nome=?
        WHERE id=?
        """, (nome, id_colaborador))
        self.conexao.commit()

    def deletar_tarefa(self, tabela, id_tarefa):
        """
        Deleta uma tarefa no banco de dados.

        :param tabela: Nome da tabela a ser deletada.
        :param id_tarefa: ID da tarefa a ser deletada.
        """
        self.cursor.execute(f"""
        DELETE FROM {tabela} WHERE id=?
        """, (id_tarefa,))
        self.conexao.commit()

    def deletar_colaborador(self, id_colaborador):
        """
        Deleta um colaborador no banco de dados.

        :param id_colaborador: ID do colaborador a ser deletado.
        """
        self.cursor.execute("""
        DELETE FROM colaboradores WHERE id=?
        """, (id_colaborador,))
        self.conexao.commit()

    def deletar_todas_tarefas(self, tabela):
        """
        Deleta todas as tarefas de uma tabela no banco de dados.

        :param tabela: Nome da tabela a ser deletada.
        """
        self.cursor.execute(f"""
        DELETE FROM {tabela}
        """)
        self.conexao.commit()

    def fechar(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.conexao.close()
