import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from database import GerenciadorBancoDeDados

class AplicativoScrum:
    def __init__(self, raiz):
        """Inicializa a interface do aplicativo e configura os widgets."""
        self.raiz = raiz
        self.raiz.title("Ferramenta de Gestão Scrum")
        self.raiz.geometry("900x400")
        self.raiz.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.gerenciador_db = GerenciadorBancoDeDados()
        self.criar_widgets()
        self.raiz.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def criar_widgets(self):
        """Cria os quadros principais da interface do usuário."""
        self.quadro_principal = ctk.CTkFrame(self.raiz)
        self.quadro_principal.pack(fill="both", expand=True)

        self.quadro_menu = ctk.CTkFrame(self.quadro_principal, width=200, corner_radius=0)
        self.quadro_menu.pack(side="left", fill="y")

        self.quadro_conteudo = ctk.CTkFrame(self.quadro_principal)
        self.quadro_conteudo.pack(side="right", fill="both", expand=True)

        self.criar_menu()
        self.mostrar_relatorio_dia()

    def criar_menu(self):
        """Cria o menu de navegação do aplicativo."""
        self.rotulo_menu = ctk.CTkLabel(self.quadro_menu, text="Menu", font=("Arial", 20))
        self.rotulo_menu.pack(pady=20)

        self.botoes_menu = [
            ctk.CTkButton(self.quadro_menu, text="Relatório do Dia", command=self.mostrar_relatorio_dia),
            ctk.CTkButton(self.quadro_menu, text="Relatórios Salvos", command=self.mostrar_relatorios_salvos),
            ctk.CTkButton(self.quadro_menu, text="Configurações", command=self.mostrar_configuracoes),
            ctk.CTkButton(self.quadro_menu, text="Gerenciar Tarefas", command=self.mostrar_gerenciar_tarefas),
            ctk.CTkButton(self.quadro_menu, text="Colaboradores", command=self.mostrar_colaboradores)
        ]

        for botao in self.botoes_menu:
            botao.pack(pady=10, padx=20, fill="x")

    def limpar_quadro_conteudo(self):
        """Limpa o conteúdo do quadro principal."""
        for widget in self.quadro_conteudo.winfo_children():
            widget.destroy()

    def mostrar_relatorio_dia(self):
        """Mostra a interface para adicionar e visualizar tarefas do dia."""
        self.limpar_quadro_conteudo()
        self.criar_widgets_relatorio_dia()
        self.quadro_conteudo.pack_propagate(False)

    def mostrar_relatorios_salvos(self):
        """Mostra os relatórios salvos."""
        self.limpar_quadro_conteudo()
        self.criar_widgets_relatorios_salvos()
        self.quadro_conteudo.pack_propagate(False)

    def mostrar_configuracoes(self):
        """Mostra a interface para adicionar configurações de tarefas e colaboradores."""
        self.limpar_quadro_conteudo()
        self.criar_widgets_configuracoes()
        self.quadro_conteudo.pack_propagate(False)

    def mostrar_gerenciar_tarefas(self):
        """Mostra a interface para gerenciar tarefas configuradas."""
        self.limpar_quadro_conteudo()
        self.criar_widgets_gerenciar_tarefas()
        self.quadro_conteudo.pack_propagate(False)

    def mostrar_colaboradores(self):
        """Mostra a interface para gerenciar colaboradores."""
        self.limpar_quadro_conteudo()
        self.criar_widgets_colaboradores()
        self.quadro_conteudo.pack_propagate(False)

    def criar_widgets_relatorio_dia(self):
        """Cria os widgets para a aba de relatório do dia."""
        self.rotulo_nome = ctk.CTkLabel(self.quadro_conteudo, text="Nome")
        self.rotulo_nome.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.colaboradores = self.gerenciador_db.buscar_colaboradores()
        self.variavel_nome = tk.StringVar()
        self.selecionar_nome = ctk.CTkOptionMenu(
            self.quadro_conteudo,
            variable=self.variavel_nome,
            values=[colaborador[1] for colaborador in self.colaboradores],
            width=180,
            height=30,
            corner_radius=8
        )
        self.selecionar_nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew", columnspan=3)

        self.rotulo_tarefa = ctk.CTkLabel(self.quadro_conteudo, text="Tarefa")
        self.rotulo_tarefa.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.tarefas_config = self.gerenciador_db.buscar_tarefas_config()
        self.variavel_tarefa = tk.StringVar()
        self.selecionar_tarefa = ctk.CTkOptionMenu(
            self.quadro_conteudo,
            variable=self.variavel_tarefa,
            values=[tarefa[1] for tarefa in self.tarefas_config],
            width=180,
            height=30,
            corner_radius=8
        )
        self.selecionar_tarefa.grid(row=1, column=1, padx=10, pady=5, sticky="ew", columnspan=3)

        self.rotulo_quantidade = ctk.CTkLabel(self.quadro_conteudo, text="Quantidade")
        self.rotulo_quantidade.grid(row=1, column=2, padx=10, pady=5, sticky="e")

        self.entrada_quantidade = ctk.CTkEntry(self.quadro_conteudo)
        self.entrada_quantidade.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        self.botao_adicionar_tarefa = ctk.CTkButton(self.quadro_conteudo, text="+", width=20, command=self.adicionar_tarefa_dia)
        self.botao_adicionar_tarefa.grid(row=1, column=4, padx=10, pady=5)

        self.criar_lista_tarefas_dia(self.quadro_conteudo)

        self.quadro_botoes = ctk.CTkFrame(self.quadro_conteudo)
        self.quadro_botoes.grid(row=3, column=0, columnspan=5, pady=10)

        self.botao_salvar = ctk.CTkButton(self.quadro_botoes, text="Salvar Relatório", command=self.salvar_tarefas_dia)
        self.botao_salvar.grid(row=0, column=0, padx=5, pady=5)

        self.botao_remover_todas = ctk.CTkButton(self.quadro_botoes, text="Remover Todas as Tarefas", command=self.confirmar_remover_todas_tarefas_dia)
        self.botao_remover_todas.grid(row=0, column=1, padx=5, pady=5)

        self.botao_gerar_relatorio = ctk.CTkButton(self.quadro_botoes, text="Gerar Relatório", command=self.gerar_relatorio)
        self.botao_gerar_relatorio.grid(row=0, column=2, padx=5, pady=5)

        self.quadro_conteudo.grid_rowconfigure(2, weight=1)
        self.quadro_conteudo.grid_columnconfigure(1, weight=1)

    def criar_lista_tarefas_dia(self, pai):
        """Cria a lista visual para exibir as tarefas do dia."""
        self.quadro_lista_dia = ctk.CTkFrame(pai)
        self.quadro_lista_dia.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        self.canvas_lista_dia = tk.Canvas(self.quadro_lista_dia, bg="#2b2b2b", highlightthickness=0)
        self.canvas_lista_dia.pack(side="left", fill="both", expand=True)

        self.scrollbar_dia = ctk.CTkScrollbar(self.quadro_lista_dia, command=self.canvas_lista_dia.yview)
        self.scrollbar_dia.pack(side="right", fill="y")

        self.canvas_lista_dia.configure(yscrollcommand=self.scrollbar_dia.set)
        self.canvas_lista_dia.bind("<Configure>", lambda e: self.canvas_lista_dia.config(scrollregion=self.canvas_lista_dia.bbox("all")))

        self.quadro_canvas_dia = ctk.CTkFrame(self.canvas_lista_dia)
        self.canvas_lista_dia.create_window((0, 0), window=self.quadro_canvas_dia, anchor="nw")

        self.quadros_tarefas_dia = []
        self.carregar_tarefas_dia()

    def carregar_tarefas_dia(self):
        """Carrega as tarefas do dia no quadro correspondente."""
        if not hasattr(self, 'quadro_canvas_dia'):
            return

        for quadro_tarefa in self.quadros_tarefas_dia:
            quadro_tarefa.destroy()
        self.quadros_tarefas_dia = []

        tarefas = self.gerenciador_db.buscar_tarefas_dia()
        for tarefa in tarefas:
            quadro_tarefa = ctk.CTkFrame(self.quadro_canvas_dia, fg_color="#3b3b3b", height=40)
            quadro_tarefa.pack(fill="x", padx=10, pady=5)

            rotulo_nome = ctk.CTkLabel(quadro_tarefa, text=tarefa[1], anchor="w", width=150)
            rotulo_nome.pack(side="left", padx=10)

            rotulo_tarefa = ctk.CTkLabel(quadro_tarefa, text=tarefa[2], anchor="w", width=150)
            rotulo_tarefa.pack(side="left", padx=10)

            rotulo_quantidade = ctk.CTkLabel(quadro_tarefa, text=str(tarefa[4]), anchor="w", width=100)
            rotulo_quantidade.pack(side="left", padx=10)

            tamanho_icone = (16, 16)
            icone_editar = self.criar_icone("icons/edit_icon.png", tamanho_icone)
            botao_editar = ctk.CTkButton(quadro_tarefa, text="", image=icone_editar, width=16, command=lambda idx=tarefa[0]: self.abrir_janela_editar_tarefa_dia(idx))
            botao_editar.pack(side="right", padx=5)
            botao_editar.bind("<Enter>", lambda e: self.mostrar_tooltip(botao_editar, "Editar"))
            botao_editar.bind("<Leave>", lambda e: self.ocultar_tooltip())

            icone_apagar = self.criar_icone("icons/delete_icon.png", tamanho_icone)
            botao_apagar = ctk.CTkButton(quadro_tarefa, text="", image=icone_apagar, width=16, command=lambda idx=tarefa[0]: self.deletar_tarefa_dia(idx))
            botao_apagar.pack(side="right", padx=5)
            botao_apagar.bind("<Enter>", lambda e: self.mostrar_tooltip(botao_apagar, "Apagar"))
            botao_apagar.bind("<Leave>", lambda e: self.ocultar_tooltip())

            self.quadros_tarefas_dia.append(quadro_tarefa)

    def adicionar_tarefa_dia(self):
        """Adiciona uma nova tarefa ao relatório do dia."""
        nome = self.variavel_nome.get()
        tarefa = self.variavel_tarefa.get()
        quantidade = self.entrada_quantidade.get()

        if not nome or not tarefa or not quantidade:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
            return

        self.gerenciador_db.adicionar_tarefa_dia(nome, tarefa, "quantidade", quantidade)
        self.carregar_tarefas_dia()
        self.limpar_entradas_dia()

    def limpar_entradas_dia(self):
        """Limpa os campos de entrada do relatório do dia."""
        self.variavel_nome.set("")
        self.variavel_tarefa.set("")
        self.entrada_quantidade.delete(0, tk.END)

    def salvar_tarefas_dia(self):
        """Salva o relatório do dia em um arquivo JSON."""
        tarefas = self.gerenciador_db.buscar_tarefas_dia()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        messagebox.showinfo("Salvo", f'Relatório salvo em reports/report_{timestamp}.json')
        with open(f'reports/report_{timestamp}.json', 'w') as file:
            json.dump([{"nome": tarefa[1], "tarefa": tarefa[2], "tipo": tarefa[3], "quantidade": tarefa[4]} for tarefa in tarefas], file)
        self.carregar_relatorios_salvos()

    def confirmar_remover_todas_tarefas_dia(self):
        """Confirma a remoção de todas as tarefas do dia."""
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover todas as tarefas?"):
            self.remover_todas_tarefas_dia()

    def remover_todas_tarefas_dia(self):
        """Remove todas as tarefas do dia."""
        self.gerenciador_db.deletar_todas_tarefas('tarefas_dia')
        self.carregar_tarefas_dia()

    def deletar_tarefa_dia(self, id_tarefa):
        """Deleta uma tarefa específica do dia."""
        self.gerenciador_db.deletar_tarefa('tarefas_dia', id_tarefa)
        self.carregar_tarefas_dia()

    def criar_widgets_relatorios_salvos(self):
        """Cria os widgets para visualizar relatórios salvos."""
        self.quadro_lista_relatorios = ctk.CTkFrame(self.quadro_conteudo)
        self.quadro_lista_relatorios.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas_relatorios = tk.Canvas(self.quadro_lista_relatorios, bg="#2b2b2b", highlightthickness=0)
        self.canvas_relatorios.pack(side="left", fill="both", expand=True)

        self.scrollbar_relatorios = ctk.CTkScrollbar(self.quadro_lista_relatorios, command=self.canvas_relatorios.yview)
        self.scrollbar_relatorios.pack(side="right", fill="y")

        self.canvas_relatorios.configure(yscrollcommand=self.scrollbar_relatorios.set)
        self.canvas_relatorios.bind("<Configure>", lambda e: self.canvas_relatorios.config(scrollregion=self.canvas_relatorios.bbox("all")))

        self.quadro_canvas_relatorios = ctk.CTkFrame(self.canvas_relatorios)
        self.canvas_relatorios.create_window((0, 0), window=self.quadro_canvas_relatorios, anchor="nw")

        self.carregar_relatorios_salvos()

    def carregar_relatorios_salvos(self):
        """Carrega os relatórios salvos na interface."""
        for widget in self.quadro_canvas_relatorios.winfo_children():
            widget.destroy()

        for file in os.listdir('reports'):
            if file.endswith('.json'):
                quadro_relatorio = ctk.CTkFrame(self.quadro_canvas_relatorios, fg_color="#3b3b3b", height=40)
                quadro_relatorio.pack(fill="x", padx=10, pady=5)

                rotulo_relatorio = ctk.CTkLabel(quadro_relatorio, text=file, anchor="w", width=300)
                rotulo_relatorio.pack(side="left", padx=10)

                icone_salvar = self.criar_icone("icons/save_icon.png", (16, 16))
                botao_salvar = ctk.CTkButton(quadro_relatorio, text="", image=icone_salvar, width=16, command=lambda f=file: self.salvar_relatorio_csv(f))
                botao_salvar.pack(side="right", padx=5)

    def salvar_relatorio_csv(self, file):
        """Salva o relatório em formato CSV."""
        with open(f'reports/{file}', 'r') as json_file:
            data = json.load(json_file)

        df = pd.DataFrame(data)
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            df.to_csv(save_path, index=False)
            messagebox.showinfo("Sucesso", f'Relatório salvo em {save_path}')

    def criar_widgets_configuracoes(self):
        """Cria os widgets para configurar tarefas e colaboradores."""
        quadro_formularios = ctk.CTkFrame(self.quadro_conteudo)
        quadro_formularios.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        quadro_tarefas = ctk.CTkFrame(quadro_formularios, fg_color="#2b2b2b")
        quadro_tarefas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        rotulo_tarefas = ctk.CTkLabel(quadro_tarefas, text="Adicionar Tarefa", font=("Arial", 16))
        rotulo_tarefas.grid(row=0, column=0, columnspan=2, pady=(10, 10))

        rotulo_nome_tarefa = ctk.CTkLabel(quadro_tarefas, text="Nome da Tarefa")
        rotulo_nome_tarefa.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entrada_nome_tarefa = ctk.CTkEntry(quadro_tarefas, corner_radius=8, width=180)
        self.entrada_nome_tarefa.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        rotulo_meta_tarefa = ctk.CTkLabel(quadro_tarefas, text="Meta")
        rotulo_meta_tarefa.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entrada_meta_tarefa = ctk.CTkEntry(quadro_tarefas, corner_radius=8, width=180)
        self.entrada_meta_tarefa.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        rotulo_prazo_tarefa = ctk.CTkLabel(quadro_tarefas, text="Prazo (dias)")
        rotulo_prazo_tarefa.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.entrada_prazo_tarefa = ctk.CTkEntry(quadro_tarefas, corner_radius=8, width=180)
        self.entrada_prazo_tarefa.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        quadro_tipo_tarefa = ctk.CTkFrame(quadro_tarefas, fg_color="#2b2b2b")
        quadro_tipo_tarefa.grid(row=4, column=0, columnspan=2, pady=10)

        self.var_tipo_tarefa = tk.StringVar(value="quantidade")
        rotulo_tipo_tarefa = ctk.CTkLabel(quadro_tipo_tarefa, text="Tipo de Tarefa")
        rotulo_tipo_tarefa.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.radio_tipo_quantidade = ctk.CTkRadioButton(quadro_tipo_tarefa, text="Quantidade", variable=self.var_tipo_tarefa, value="quantidade")
        self.radio_tipo_quantidade.grid(row=0, column=1, padx=10, pady=5)

        self.radio_tipo_tempo = ctk.CTkRadioButton(quadro_tipo_tarefa, text="Tempo", variable=self.var_tipo_tarefa, value="tempo")
        self.radio_tipo_tempo.grid(row=0, column=2, padx=10, pady=5)

        botao_adicionar_tarefa = ctk.CTkButton(quadro_tarefas, text="Adicionar Tarefa", command=self.adicionar_tarefa_config)
        botao_adicionar_tarefa.grid(row=5, column=0, columnspan=2, pady=(10, 10))

        quadro_colaboradores = ctk.CTkFrame(quadro_formularios, fg_color="#2b2b2b")
        quadro_colaboradores.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        rotulo_colaboradores = ctk.CTkLabel(quadro_colaboradores, text="Adicionar Colaborador", font=("Arial", 16))
        rotulo_colaboradores.grid(row=0, column=0, columnspan=2, pady=(10, 10))

        rotulo_nome_colaborador = ctk.CTkLabel(quadro_colaboradores, text="Nome Completo")
        rotulo_nome_colaborador.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entrada_nome_colaborador = ctk.CTkEntry(quadro_colaboradores, corner_radius=8, width=180)
        self.entrada_nome_colaborador.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        botao_adicionar_colaborador = ctk.CTkButton(quadro_colaboradores, text="Adicionar Colaborador", command=self.adicionar_colaborador)
        botao_adicionar_colaborador.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        quadro_formularios.grid_columnconfigure(0, weight=1)
        quadro_formularios.grid_columnconfigure(1, weight=1)

    def adicionar_tarefa_config(self):
        """Adiciona uma nova tarefa de configuração ao banco de dados."""
        nome_tarefa = self.entrada_nome_tarefa.get()
        meta_tarefa = self.entrada_meta_tarefa.get()
        prazo_tarefa = self.entrada_prazo_tarefa.get()

        if not nome_tarefa or not meta_tarefa or not prazo_tarefa:
            messagebox.showerror("Erro", "Todos os campos de tarefa devem ser preenchidos.")
            return

        tipo_tarefa = self.var_tipo_tarefa.get()

        try:
            quantidade = int(meta_tarefa) if tipo_tarefa == "quantidade" else float(meta_tarefa)
            prazo = int(prazo_tarefa)
        except ValueError:
            messagebox.showerror("Erro", "Meta e prazo devem ser números.")
            return

        self.gerenciador_db.adicionar_tarefa_config(nome_tarefa, nome_tarefa, tipo_tarefa, quantidade, prazo)
        self.carregar_tarefas_para_gerenciar()
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso.")
        self.entrada_nome_tarefa.delete(0, tk.END)
        self.entrada_meta_tarefa.delete(0, tk.END)
        self.entrada_prazo_tarefa.delete(0, tk.END)

    def criar_widgets_gerenciar_tarefas(self):
        """Cria os widgets para gerenciar tarefas configuradas."""
        rotulo_gerenciar_tarefas = ctk.CTkLabel(self.quadro_conteudo, text="Gerenciar Tarefas", font=("Arial", 20))
        rotulo_gerenciar_tarefas.pack(pady=10)

        self.quadro_lista_tarefas = ctk.CTkFrame(self.quadro_conteudo)
        self.quadro_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas_tarefas = tk.Canvas(self.quadro_lista_tarefas, bg="#2b2b2b", highlightthickness=0)
        self.canvas_tarefas.pack(side="left", fill="both", expand=True)

        self.scrollbar_tarefas = ctk.CTkScrollbar(self.quadro_lista_tarefas, command=self.canvas_tarefas.yview)
        self.scrollbar_tarefas.pack(side="right", fill="y")

        self.canvas_tarefas.configure(yscrollcommand=self.scrollbar_tarefas.set)
        self.canvas_tarefas.bind("<Configure>", lambda e: self.canvas_tarefas.config(scrollregion=self.canvas_tarefas.bbox("all")))

        self.quadro_canvas_tarefas = ctk.CTkFrame(self.canvas_tarefas)
        self.canvas_tarefas.create_window((0, 0), window=self.quadro_canvas_tarefas, anchor="nw")

        self.carregar_tarefas_para_gerenciar()

    def carregar_tarefas_para_gerenciar(self):
        """Carrega as tarefas configuradas no quadro correspondente."""
        if not hasattr(self, 'quadro_canvas_tarefas'):
            return

        for quadro_tarefa in self.quadro_canvas_tarefas.winfo_children():
            quadro_tarefa.destroy()

        tarefas = self.gerenciador_db.buscar_tarefas_config()
        for tarefa in tarefas:
            quadro_tarefa = ctk.CTkFrame(self.quadro_canvas_tarefas, fg_color="#3b3b3b", height=40)
            quadro_tarefa.pack(fill="x", padx=10, pady=5)

            rotulo_nome = ctk.CTkLabel(quadro_tarefa, text=tarefa[1], anchor="w", width=150)
            rotulo_nome.pack(side="left", padx=10)

            rotulo_tarefa = ctk.CTkLabel(quadro_tarefa, text=tarefa[2], anchor="w", width=150)
            rotulo_tarefa.pack(side="left", padx=10)

            rotulo_quantidade = ctk.CTkLabel(quadro_tarefa, text=str(tarefa[4]), anchor="w", width=100)
            rotulo_quantidade.pack(side="left", padx=10)

            rotulo_prazo = ctk.CTkLabel(quadro_tarefa, text=f"Prazo: {tarefa[5]} dias", anchor="w", width=100)
            rotulo_prazo.pack(side="left", padx=10)

            tamanho_icone = (16, 16)
            icone_editar = self.criar_icone("icons/edit_icon.png", tamanho_icone)
            botao_editar = ctk.CTkButton(quadro_tarefa, text="", image=icone_editar, width=16, command=lambda idx=tarefa[0]: self.abrir_janela_editar_tarefa_config(idx))
            botao_editar.pack(side="right", padx=5)
            botao_editar.bind("<Enter>", lambda e: self.mostrar_tooltip(botao_editar, "Editar"))
            botao_editar.bind("<Leave>", lambda e: self.ocultar_tooltip())

            icone_apagar = self.criar_icone("icons/delete_icon.png", tamanho_icone)
            botao_apagar = ctk.CTkButton(quadro_tarefa, text="", image=icone_apagar, width=16, command=lambda idx=tarefa[0]: self.deletar_tarefa_config(idx))
            botao_apagar.pack(side="right", padx=5)
            botao_apagar.bind("<Enter>", lambda e: self.mostrar_tooltip(botao_apagar, "Apagar"))
            botao_apagar.bind("<Leave>", lambda e: self.ocultar_tooltip())

    def deletar_tarefa_config(self, id_tarefa):
        """Deleta uma tarefa de configuração específica."""
        self.gerenciador_db.deletar_tarefa('tarefas_config', id_tarefa)
        self.carregar_tarefas_para_gerenciar()

    def criar_widgets_colaboradores(self):
        """Cria os widgets para gerenciar colaboradores."""
        rotulo_colaboradores = ctk.CTkLabel(self.quadro_conteudo, text="Colaboradores", font=("Arial", 20))
        rotulo_colaboradores.pack(pady=10)

        self.quadro_lista_colaboradores = ctk.CTkFrame(self.quadro_conteudo)
        self.quadro_lista_colaboradores.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas_colaboradores = tk.Canvas(self.quadro_lista_colaboradores, bg="#2b2b2b", highlightthickness=0)
        self.canvas_colaboradores.pack(side="left", fill="both", expand=True)

        self.scrollbar_colaboradores = ctk.CTkScrollbar(self.quadro_lista_colaboradores, command=self.canvas_colaboradores.yview)
        self.scrollbar_colaboradores.pack(side="right", fill="y")

        self.canvas_colaboradores.configure(yscrollcommand=self.scrollbar_colaboradores.set)
        self.canvas_colaboradores.bind("<Configure>", lambda e: self.canvas_colaboradores.config(scrollregion=self.canvas_colaboradores.bbox("all")))

        self.quadro_canvas_colaboradores = ctk.CTkFrame(self.canvas_colaboradores)
        self.canvas_colaboradores.create_window((0, 0), window=self.quadro_canvas_colaboradores, anchor="nw")

        self.carregar_colaboradores()

    def carregar_colaboradores(self):
        """Carrega os colaboradores no quadro correspondente."""
        if not hasattr(self, 'quadro_canvas_colaboradores'):
            return

        for quadro_colaborador in self.quadro_canvas_colaboradores.winfo_children():
            quadro_colaborador.destroy()

        colaboradores = self.gerenciador_db.buscar_colaboradores()
        for colaborador in colaboradores:
            quadro_colaborador = ctk.CTkFrame(self.quadro_canvas_colaboradores, fg_color="#3b3b3b", height=40)
            quadro_colaborador.pack(fill="x", padx=10, pady=5)

            rotulo_nome_colaborador = ctk.CTkLabel(quadro_colaborador, text=colaborador[1], anchor="w", width=150)
            rotulo_nome_colaborador.pack(side="left", padx=10)

            tamanho_icone = (16, 16)
            icone_editar = self.criar_icone("icons/edit_icon.png", tamanho_icone)
            botao_editar = ctk.CTkButton(quadro_colaborador, text="", image=icone_editar, width=16, command=lambda idx=colaborador[0]: self.abrir_janela_editar_colaborador(idx))
            botao_editar.pack(side="right", padx=5)
            botao_editar.bind("<Enter>", lambda e: self.mostrar_tooltip(botao_editar, "Editar"))
            botao_editar.bind("<Leave>", lambda e: self.ocultar_tooltip())

            icone_apagar = self.criar_icone("icons/delete_icon.png", tamanho_icone)
            botao_apagar = ctk.CTkButton(quadro_colaborador, text="", image=icone_apagar, width=16, command=lambda idx=colaborador[0]: self.deletar_colaborador(idx))
            botao_apagar.pack(side="right", padx=5)
            botao_apagar.bind("<Enter>", lambda e: self.mostrar_tooltip(botao_apagar, "Apagar"))
            botao_apagar.bind("<Leave>", lambda e: self.ocultar_tooltip())

    def abrir_janela_editar_tarefa_dia(self, id_tarefa):
        """Abre a janela para editar uma tarefa do dia."""
        tarefa = self.gerenciador_db.buscar_tarefa_por_id('tarefas_dia', id_tarefa)
        if tarefa:
            janela_editar = ctk.CTkToplevel(self.raiz)
            janela_editar.title("Editar Tarefa")

            rotulo_nome = ctk.CTkLabel(janela_editar, text="Nome")
            rotulo_nome.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            entrada_nome = ctk.CTkEntry(janela_editar)
            entrada_nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
            entrada_nome.insert(0, tarefa[1])

            rotulo_tarefa = ctk.CTkLabel(janela_editar, text="Tarefa")
            rotulo_tarefa.grid(row=1, column=0, padx=10, pady=5, sticky="e")
            entrada_tarefa = ctk.CTkEntry(janela_editar)
            entrada_tarefa.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
            entrada_tarefa.insert(0, tarefa[2])

            rotulo_quantidade = ctk.CTkLabel(janela_editar, text="Quantidade")
            rotulo_quantidade.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            entrada_quantidade = ctk.CTkEntry(janela_editar)
            entrada_quantidade.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
            entrada_quantidade.insert(0, tarefa[4])

            botao_salvar = ctk.CTkButton(janela_editar, text="Salvar", command=lambda: self.salvar_edicao_tarefa_dia(id_tarefa, entrada_nome.get(), entrada_tarefa.get(), entrada_quantidade.get(), janela_editar))
            botao_salvar.grid(row=3, column=0, padx=10, pady=10)

            botao_cancelar = ctk.CTkButton(janela_editar, text="Cancelar", command=janela_editar.destroy)
            botao_cancelar.grid(row=3, column=1, padx=10, pady=10)

    def abrir_janela_editar_tarefa_config(self, id_tarefa):
        """Abre a janela para editar uma tarefa de configuração."""
        tarefa = self.gerenciador_db.buscar_tarefa_por_id('tarefas_config', id_tarefa)
        if tarefa:
            janela_editar = ctk.CTkToplevel(self.raiz)
            janela_editar.title("Editar Tarefa Configuração")

            rotulo_nome = ctk.CTkLabel(janela_editar, text="Nome da Tarefa")
            rotulo_nome.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            entrada_nome = ctk.CTkEntry(janela_editar)
            entrada_nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
            entrada_nome.insert(0, tarefa[1])

            rotulo_quantidade = ctk.CTkLabel(janela_editar, text="Meta")
            rotulo_quantidade.grid(row=1, column=0, padx=10, pady=5, sticky="e")
            entrada_quantidade = ctk.CTkEntry(janela_editar)
            entrada_quantidade.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
            entrada_quantidade.insert(0, tarefa[4])

            rotulo_prazo = ctk.CTkLabel(janela_editar, text="Prazo (dias)")
            rotulo_prazo.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            entrada_prazo = ctk.CTkEntry(janela_editar)
            entrada_prazo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
            entrada_prazo.insert(0, tarefa[5])

            botao_salvar = ctk.CTkButton(janela_editar, text="Salvar", command=lambda: self.salvar_edicao_tarefa_config(id_tarefa, entrada_nome.get(), entrada_quantidade.get(), entrada_prazo.get(), janela_editar))
            botao_salvar.grid(row=3, column=0, padx=10, pady=10)

            botao_cancelar = ctk.CTkButton(janela_editar, text="Cancelar", command=janela_editar.destroy)
            botao_cancelar.grid(row=3, column=1, padx=10, pady=10)

    def abrir_janela_editar_colaborador(self, id_colaborador):
        """Abre a janela para editar um colaborador."""
        colaborador = self.gerenciador_db.buscar_colaborador_por_id(id_colaborador)
        if colaborador:
            janela_editar = ctk.CTkToplevel(self.raiz)
            janela_editar.title("Editar Colaborador")

            rotulo_nome = ctk.CTkLabel(janela_editar, text="Nome Completo")
            rotulo_nome.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            entrada_nome = ctk.CTkEntry(janela_editar)
            entrada_nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
            entrada_nome.insert(0, colaborador[1])

            botao_salvar = ctk.CTkButton(janela_editar, text="Salvar", command=lambda: self.salvar_edicao_colaborador(id_colaborador, entrada_nome.get(), janela_editar))
            botao_salvar.grid(row=1, column=0, padx=10, pady=10)

            botao_cancelar = ctk.CTkButton(janela_editar, text="Cancelar", command=janela_editar.destroy)
            botao_cancelar.grid(row=1, column=1, padx=10, pady=10)

    def salvar_edicao_tarefa_dia(self, id_tarefa, nome, tarefa, quantidade, janela):
        """Salva as alterações feitas em uma tarefa do dia."""
        if messagebox.askyesno("Confirmação", "Deseja salvar as alterações?"):
            try:
                quantidade = int(quantidade)
                self.gerenciador_db.atualizar_tarefa('tarefas_dia', id_tarefa, nome, tarefa, "quantidade", quantidade)
                janela.destroy()
                self.carregar_tarefas_dia()
                messagebox.showinfo("Sucesso", "Tarefa editada com sucesso.")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")

    def salvar_edicao_tarefa_config(self, id_tarefa, nome, quantidade, prazo, janela):
        """Salva as alterações feitas em uma tarefa de configuração."""
        if messagebox.askyesno("Confirmação", "Deseja salvar as alterações?"):
            try:
                quantidade = int(quantidade)
                prazo = int(prazo)
                self.gerenciador_db.atualizar_tarefa('tarefas_config', id_tarefa, nome, nome, "quantidade", quantidade, prazo)
                janela.destroy()
                self.carregar_tarefas_para_gerenciar()
                messagebox.showinfo("Sucesso", "Tarefa de configuração editada com sucesso.")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade e prazo devem ser números inteiros.")

    def salvar_edicao_colaborador(self, id_colaborador, nome, janela):
        """Salva as alterações feitas em um colaborador."""
        if messagebox.askyesno("Confirmação", "Deseja salvar as alterações?"):
            self.gerenciador_db.atualizar_colaborador(id_colaborador, nome)
            janela.destroy()
            self.carregar_colaboradores()
            messagebox.showinfo("Sucesso", "Colaborador editado com sucesso.")

    def adicionar_colaborador(self):
        """Adiciona um novo colaborador ao banco de dados."""
        nome_colaborador = self.entrada_nome_colaborador.get()

        if not nome_colaborador:
            messagebox.showerror("Erro", "O nome do colaborador deve ser preenchido.")
            return

        partes_nome = nome_colaborador.split()
        if len(partes_nome) < 2:
            messagebox.showerror("Erro", "Insira pelo menos nome e sobrenome.")
            return

        nome_formatado = ' '.join(parte.capitalize() for parte in partes_nome)

        if self.gerenciador_db.verificar_colaborador_existente(nome_formatado):
            messagebox.showerror("Erro", "Colaborador já existe.")
            return

        self.gerenciador_db.adicionar_colaborador(nome_formatado)
        self.carregar_colaboradores()
        messagebox.showinfo("Sucesso", "Colaborador adicionado com sucesso.")
        self.entrada_nome_colaborador.delete(0, tk.END)

    def gerar_relatorio(self):
        """Gera gráficos de metas para as tarefas configuradas."""
        tarefas_config = self.gerenciador_db.buscar_tarefas_config()
        for tarefa in tarefas_config:
            self.gerar_grafico_meta(tarefa)

    def gerar_grafico_meta(self, tarefa):
        """Gera um gráfico para uma meta específica de tarefa."""
        nome_tarefa = tarefa[1]
        meta = tarefa[4]
        prazo = tarefa[5]

        dias = list(range(1, prazo + 1))
        progresso = [0] * prazo
        base = [meta * (i + 1) / prazo for i in range(prazo)]

        tarefas_dia = self.gerenciador_db.buscar_tarefas_dia_por_nome(nome_tarefa)
        for t in tarefas_dia:
            try:
                dia = min((datetime.now() - datetime.strptime(t[5], "%Y-%m-%d")).days, prazo - 1)
                progresso[dia] += int(t[4])
            except ValueError:
                messagebox.showerror("Erro", f"Quantidade inválida para a tarefa: {t[1]}")

        progresso_acumulado = [sum(progresso[:i + 1]) for i in range(prazo)]

        figura, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dias, base, label='Meta', linestyle='--', color='gray')
        ax.plot(dias, progresso_acumulado, label='Progresso', color='blue')
        ax.fill_between(dias, progresso_acumulado, base, where=(progresso_acumulado < base), color='red', alpha=0.3)
        ax.fill_between(dias, progresso_acumulado, base, where=(progresso_acumulado >= base), color='green', alpha=0.3)
        ax.set_title(f'Meta: {nome_tarefa}')
        ax.set_xlabel('Dias')
        ax.set_ylabel('Quantidade')
        ax.legend()

        janela_grafico = ctk.CTkToplevel(self.raiz)
        janela_grafico.title(f'Relatório: {nome_tarefa}')

        canvas = FigureCanvasTkAgg(figura, janela_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        botao_salvar = ctk.CTkButton(janela_grafico, text="Salvar Gráfico", command=lambda: self.salvar_grafico(figura))
        botao_salvar.pack(pady=10)

    def salvar_grafico(self, figura):
        """Salva o gráfico gerado em um arquivo PNG."""
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            figura.savefig(save_path)
            messagebox.showinfo("Sucesso", f'Gráfico salvo em {save_path}')

    def ao_fechar(self):
        """Fecha a aplicação e a conexão com o banco de dados."""
        self.gerenciador_db.fechar()
        self.raiz.destroy()

    def criar_icone(self, caminho, tamanho):
        """Cria um ícone redimensionado para uso na interface."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=tamanho)

    def mostrar_tooltip(self, widget, texto):
        """Mostra um tooltip de ajuda sobre um botão."""
        self.tooltip = tk.Toplevel(widget)
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{widget.winfo_rootx() + 20}+{widget.winfo_rooty() + 20}")
        rotulo = ctk.CTkLabel(self.tooltip, text=texto, justify='left')
        rotulo.pack()

    def ocultar_tooltip(self):
        """Oculta o tooltip de ajuda."""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

if __name__ == "__main__":
    # Inicializa a aplicação principal
    raiz = ctk.CTk()
    app = AplicativoScrum(raiz)
    raiz.mainloop()
