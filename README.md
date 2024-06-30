# Ferramenta de Gestão Scrum

## Visão Geral

Esta aplicação é uma ferramenta de gerenciamento de tarefas usando a metodologia Scrum, desenvolvida com `customtkinter` e `tkinter`. O aplicativo permite gerenciar tarefas diárias, colaboradores e gerar relatórios.

## Estrutura do Código

### Arquivo `app.py`

#### Classes e Funções

- **`class AplicativoScrum`**: Classe principal da aplicação, responsável por gerenciar a interface do usuário e a interação com o banco de dados.

- **`__init__(self, raiz)`**: Inicializa a aplicação, configurando a janela principal e o banco de dados.
  - **Parâmetros**:
    - `raiz`: Janela principal do Tkinter.

- **`criar_widgets(self)`**: Cria os widgets principais da aplicação, incluindo o menu e a área de conteúdo.

- **`criar_menu(self)`**: Cria os botões do menu para navegação entre as seções do aplicativo.

- **`limpar_quadro_conteudo(self)`**: Limpa todos os widgets do quadro de conteúdo.

- **`mostrar_relatorio_dia(self)`**: Exibe a seção de relatório do dia na interface.

- **`mostrar_relatorios_salvos(self)`**: Exibe a seção de relatórios salvos.

- **`mostrar_configuracoes(self)`**: Exibe a seção de configurações.

- **`mostrar_gerenciar_tarefas(self)`**: Exibe a seção para gerenciar tarefas.

- **`mostrar_colaboradores(self)`**: Exibe a seção de colaboradores.

- **`criar_widgets_relatorio_dia(self)`**: Cria os widgets para a seção de relatório do dia, permitindo seleção de nome, tarefa e quantidade.

- **`criar_lista_tarefas_dia(self, pai)`**: Cria a lista de tarefas do dia em um quadro rolável.
  - **Parâmetros**:
    - `pai`: Widget pai onde a lista será inserida.

- **`carregar_tarefas_dia(self)`**: Carrega as tarefas do dia do banco de dados e exibe na interface.

- **`adicionar_tarefa_dia(self)`**: Adiciona uma nova tarefa diária ao banco de dados.

- **`limpar_entradas_dia(self)`**: Limpa as entradas da seção de relatório do dia.

- **`salvar_tarefas_dia(self)`**: Salva as tarefas do dia em um arquivo JSON.

- **`confirmar_remover_todas_tarefas_dia(self)`**: Confirmação para remover todas as tarefas do dia.

- **`remover_todas_tarefas_dia(self)`**: Remove todas as tarefas do dia do banco de dados.

- **`deletar_tarefa_dia(self, id_tarefa)`**: Deleta uma tarefa específica do dia.
  - **Parâmetros**:
    - `id_tarefa`: ID da tarefa a ser deletada.

- **`criar_widgets_relatorios_salvos(self)`**: Cria os widgets para a seção de relatórios salvos.

- **`carregar_relatorios_salvos(self)`**: Carrega e exibe os relatórios salvos em formato JSON.

- **`salvar_relatorio_csv(self, file)`**: Salva um relatório em formato CSV.
  - **Parâmetros**:
    - `file`: Nome do arquivo JSON do relatório.

- **`criar_widgets_configuracoes(self)`**: Cria os widgets para a seção de configurações, permitindo adicionar tarefas e colaboradores.

- **`adicionar_tarefa_config(self)`**: Adiciona uma nova tarefa nas configurações.
  
- **`criar_widgets_gerenciar_tarefas(self)`**: Cria os widgets para gerenciar tarefas.

- **`carregar_tarefas_para_gerenciar(self)`**: Carrega as tarefas configuradas para exibição.

- **`deletar_tarefa_config(self, id_tarefa)`**: Deleta uma tarefa de configuração específica.
  - **Parâmetros**:
    - `id_tarefa`: ID da tarefa a ser deletada.

- **`criar_widgets_colaboradores(self)`**: Cria os widgets para gerenciar colaboradores.

- **`carregar_colaboradores(self)`**: Carrega os colaboradores do banco de dados.

- **`abrir_janela_editar_tarefa_dia(self, id_tarefa)`**: Abre uma janela para editar uma tarefa do dia.
  - **Parâmetros**:
    - `id_tarefa`: ID da tarefa a ser editada.

- **`abrir_janela_editar_tarefa_config(self, id_tarefa)`**: Abre uma janela para editar uma tarefa de configuração.

- **`abrir_janela_editar_colaborador(self, id_colaborador)`**: Abre uma janela para editar um colaborador.

- **`salvar_edicao_tarefa_dia(self, id_tarefa, nome, tarefa, quantidade, janela)`**: Salva as alterações de uma tarefa do dia editada.

- **`salvar_edicao_tarefa_config(self, id_tarefa, nome, quantidade, prazo, janela)`**: Salva as alterações de uma tarefa de configuração editada.

- **`salvar_edicao_colaborador(self, id_colaborador, nome, janela)`**: Salva as alterações de um colaborador editado.

- **`adicionar_colaborador(self)`**: Adiciona um novo colaborador ao banco de dados.

- **`gerar_relatorio(self)`**: Gera gráficos de progresso para cada meta.

- **`gerar_grafico_meta(self, tarefa)`**: Gera um gráfico de progresso para uma meta específica.

- **`salvar_grafico(self, figura)`**: Salva um gráfico em formato PNG.

- **`ao_fechar(self)`**: Fecha a aplicação e o banco de dados.

- **`criar_icone(self, caminho, tamanho)`**: Cria um ícone a partir de uma imagem.
  - **Parâmetros**:
    - `caminho`: Caminho do arquivo de imagem.
    - `tamanho`: Tamanho do ícone.

- **`mostrar_tooltip(self, widget, texto)`**: Exibe uma dica flutuante (tooltip) sobre um widget.
  - **Parâmetros**:
    - `widget`: Widget sobre o qual a dica será exibida.
    - `texto`: Texto da dica.

- **`ocultar_tooltip(self)`**: Oculta a dica flutuante (tooltip).

### Arquivo `database.py`

#### Classes e Funções

- **`class GerenciadorBancoDeDados`**: Classe para gerenciar operações no banco de dados SQLite.

- **`__init__(self, db_name="database.db")`**: Inicializa a conexão com o banco de dados.
  - **Parâmetros**:
    - `db_name`: Nome do arquivo do banco de dados.

- **`criar_tabelas(self)`**: Cria as tabelas necessárias no banco de dados se não existirem.

- **`adicionar_tarefa_dia(self, nome, tarefa, tipo, quantidade)`**: Adiciona uma tarefa ao banco de dados para o dia.
  - **Parâmetros**:
    - `nome`: Nome do colaborador.
    - `tarefa`: Nome da tarefa.
    - `tipo`: Tipo de tarefa (quantidade ou tempo).
    - `quantidade`: Quantidade ou tempo estimado.

- **`adicionar_tarefa_config(self, nome, tarefa, tipo, quantidade, prazo)`**: Adiciona uma tarefa de configuração ao banco de dados.
  - **Parâmetros**:
    - `nome`: Nome da tarefa.
    - `tipo`: Tipo de tarefa.
    - `quantidade`: Meta de quantidade ou tempo.
    - `prazo`: Prazo em dias para conclusão.

- **`adicionar_colaborador(self, nome)`**: Adiciona um colaborador ao banco de dados.
  - **Parâmetros**:
    - `nome`: Nome completo do colaborador.

- **`atualizar_tarefa(self, tabela, id_tarefa, nome, tarefa, tipo, quantidade, prazo=None)`**: Atualiza uma tarefa no banco de dados.
  - **Parâmetros**:
    - `tabela`: Nome da tabela.
    - `id_tarefa`: ID da tarefa a ser atualizada.
    - `nome`: Nome ou título da tarefa.
    - `tarefa`: Nome da tarefa.
    - `tipo`: Tipo de tarefa.
    - `quantidade`: Meta ou quantidade atual.
    - `prazo`: Prazo em dias (opcional).

- **`atualizar_colaborador(self, id_colaborador, nome)`**: Atualiza os dados de um colaborador no banco de dados.
  - **Parâmetros**:
    - `id_colaborador`: ID do colaborador.
    - `nome`: Nome completo do colaborador.

- **`deletar_tarefa(self, tabela, id_tarefa)`**: Deleta uma tarefa do banco de dados.
  - **Parâmetros**:
    - `tabela`: Nome da tabela.
    - `id_tarefa`: ID da tarefa a ser deletada.

- **`deletar_todas_tarefas(self, tabela)`**: Deleta todas as tarefas de uma tabela específica.
  - **Parâmetros**:
    - `tabela`: Nome da tabela.

- **`buscar_tarefas_dia(self)`**: Retorna todas as tarefas do dia armazenadas no banco de dados.

- **`buscar_tarefas_config(self)`**: Retorna todas as tarefas de configuração.

- **`buscar_tarefas_dia_por_nome(self, nome_tarefa)`**: Busca tarefas do dia por nome de tarefa.

- **`buscar_colaboradores(self)`**: Retorna todos os colaboradores cadastrados.

- **`buscar_tarefa_por_id(self, tabela, id_tarefa)`**: Retorna uma tarefa específica pelo ID.
  - **Parâmetros**:
    - `tabela`: Nome da tabela.
    - `id_tarefa`: ID da tarefa.

- **`buscar_colaborador_por_id(self, id_colaborador)`**: Retorna os dados de um colaborador específico pelo ID.

- **`verificar_colaborador_existente(self, nome)`**: Verifica se um colaborador já existe no banco de dados.
  - **Parâmetros**:
    - `nome`: Nome completo do colaborador.

- **`fechar(self)`**: Fecha a conexão com o banco de dados.

## Como Usar

1. **Instalação**: Certifique-se de ter Python e as bibliotecas necessárias instaladas.
2. **Execução**: Execute o arquivo `main.py` para iniciar a aplicação.
3. **Funcionalidades**:
   - **Relatório do Dia**: Adicione e gerencie tarefas diárias.
   - **Relatórios Salvos**: Visualize relatórios salvos e exporte para CSV.
   - **Configurações**: Configure novas tarefas e adicione colaboradores.
   - **Gerenciar Tarefas**: Edite e delete tarefas existentes.
   - **Colaboradores**: Edite e delete colaboradores.

## Requisitos

- Python 3.x
- Bibliotecas:
  - customtkinter
  - tkinter
  - pandas
  - matplotlib
  - Pillow

