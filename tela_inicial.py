import customtkinter as ctk
from tkinter import ttk, messagebox, Scrollbar, Canvas
import banco
import relatorio

banco.inicializar_banco()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CollapsibleSection(ctk.CTkFrame):
    def __init__(self, master, title="Seção", max_height=160, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.visible = False

        self.button = ctk.CTkButton(self, text=title + " ▼", command=self.toggle)
        self.button.pack(fill="x")

        self.canvas = Canvas(self, height=max_height, bg="#1e1e1e", highlightthickness=0)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.canvas.pack(side="left", fill="both", expand=False)
            self.scrollbar.pack(side="right", fill="y")
            self.button.configure(text=self.button.cget("text").replace("▼", "▲"))
        else:
            self.canvas.pack_forget()
            self.scrollbar.pack_forget()
            self.button.configure(text=self.button.cget("text").replace("▲", "▼"))

    def get_frame(self):
        return self.inner_frame


class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Painel do Projeto")
        self.geometry("1000x650")
        self.projeto_selecionado = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        for col in range(3):
            self.grid_columnconfigure(col, weight=1, uniform="col")

        self.setup_styles()
        self.add_top_widgets()
        self.add_bottom_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1e1e1e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#1e1e1e",
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading",
                        background="#0078D4",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[("selected", "#005A9E")])

    def add_top_widgets(self):
        frame_opcoes = ctk.CTkFrame(self, width=280)
        frame_opcoes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_opcoes.grid_propagate(False)

        ctk.CTkLabel(frame_opcoes, text="Menu", font=("Roboto", 16)).pack(pady=10)

        # GAVETA 1 - Exportar
        exportar_section = CollapsibleSection(frame_opcoes, title="Exportar", max_height=160)
        exportar_section.pack(fill="x", pady=5)
        frame_exp = exportar_section.get_frame()

        def exportar_pdf_selecionado():
            if self.projeto_selecionado is None:
                messagebox.showwarning("Aviso", "Nenhum projeto selecionado para exportar.")
                return
            projeto = banco.carregar_projeto_por_id(self.projeto_selecionado)
            if projeto:
                relatorio.gerar_pdf_projeto(projeto)

        def exportar_csv_selecionado():
            if self.projeto_selecionado is None:
                messagebox.showwarning("Aviso", "Nenhum projeto selecionado para exportar.")
                return
            projeto = banco.carregar_projeto_por_id(self.projeto_selecionado)
            if projeto:
                relatorio.exportar_csv_projeto(projeto)

        def gerar_grafico_selecionado():
            if self.projeto_selecionado is None:
                messagebox.showwarning("Aviso", "Nenhum projeto selecionado para gerar gráfico.")
                return
            projeto = banco.carregar_projeto_por_id(self.projeto_selecionado)
            if projeto:
                relatorio.gerar_grafico_barras(projeto)

        ctk.CTkButton(frame_exp, text="Exportar PDF", command=exportar_pdf_selecionado).pack(pady=2, fill="x")
        ctk.CTkButton(frame_exp, text="Exportar CSV", command=exportar_csv_selecionado).pack(pady=2, fill="x")
        ctk.CTkButton(frame_exp, text="Gerar Gráfico", command=gerar_grafico_selecionado).pack(pady=2, fill="x")

        # GAVETA 2 - Projeto
        projeto_section = CollapsibleSection(frame_opcoes, title="Projeto", max_height=160)
        projeto_section.pack(fill="x", pady=5)
        frame_proj = projeto_section.get_frame()

        ctk.CTkButton(frame_proj, text="Novo Projeto", command=lambda: banco.adicionar_projeto(self, callback=self.atualizar_tela)).pack(pady=2, fill="x")
        ctk.CTkButton(frame_proj, text="Adicionar Etapa", command=lambda: banco.janela_adicionar_etapa(self, callback=self.atualizar_tela)).pack(pady=2, fill="x")
        ctk.CTkButton(frame_proj, text="Editar Projeto", command=self.editar_projeto_selecionado).pack(pady=2, fill="x")
        ctk.CTkButton(frame_proj, text="Excluir Projeto", command=self.excluir_projeto_selecionado).pack(pady=2, fill="x")
        ctk.CTkButton(frame_proj, text="Definir Prazo Geral", command=self.definir_prazo_geral).pack(pady=2, fill="x")

        # GAVETA 3 - Participante
        participante_section = CollapsibleSection(frame_opcoes, title="Participante", max_height=160)
        participante_section.pack(fill="x", pady=5)
        frame_part = participante_section.get_frame()

        # Aqui chamamos as funções reais do banco.py
        ctk.CTkButton(frame_part, text="Adicionar Participante", command=lambda: banco.adicionar_participante(self, self.projeto_selecionado, callback=self.atualizar_tela)).pack(pady=2, fill="x")
        ctk.CTkButton(frame_part, text="Editar Participante", command=lambda: banco.editar_participante(self, self.projeto_selecionado, callback=self.atualizar_tela)).pack(pady=2, fill="x")
        ctk.CTkButton(frame_part, text="Remover Participante", command=lambda: banco.remover_participante(self, self.projeto_selecionado, callback=self.atualizar_tela)).pack(pady=2, fill="x")

        # Frame Pessoas (col 1)
        self.frame_pessoas = ctk.CTkFrame(self)
        self.frame_pessoas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.atualizar_pessoas()

        # Frame Progresso (col 2)
        frame_prog = ctk.CTkFrame(self)
        frame_prog.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame_prog, text="Progresso do Projeto", font=("Roboto", 16)).pack(pady=10)

        self.progress_var = ctk.IntVar(value=0)
        self.progress_bar = ctk.CTkProgressBar(frame_prog, width=200, height=25)
        self.progress_bar.pack(pady=10)

        self.progress_label = ctk.CTkLabel(frame_prog, text="0%", font=("Roboto", 14))
        self.progress_label.pack()

    def editar_projeto_selecionado(self):
        if self.projeto_selecionado is None:
            messagebox.showwarning("Aviso", "Nenhum projeto selecionado para editar.")
            return
        banco.editar_projeto(self, self.projeto_selecionado, callback=self.atualizar_tela)

    def excluir_projeto_selecionado(self):
        if self.projeto_selecionado is None:
            messagebox.showwarning("Aviso", "Nenhum projeto selecionado para excluir.")
            return
        banco.excluir_projeto(self, self.projeto_selecionado, callback=self.atualizar_tela)
        self.projeto_selecionado = None
        self.atualizar_pessoas()
        self.atualizar_tela()

    def definir_prazo_geral(self):
        if self.projeto_selecionado is None:
            messagebox.showwarning("Aviso", "Nenhum projeto selecionado para definir prazo.")
            return
        banco.definir_prazo_geral(self, self.projeto_selecionado, callback=self.atualizar_tela)

    def atualizar_pessoas(self):
        for widget in self.frame_pessoas.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame_pessoas, text="Pessoas Envolvidas", font=("Roboto", 16)).pack(pady=5)

        tree_frame = ctk.CTkFrame(self.frame_pessoas)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        colunas = ("Nome", "Cargo", "Etapa", "Prazo")
        tree = ttk.Treeview(tree_frame, columns=colunas, show="headings", height=6)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        projeto = banco.carregar_projeto_por_id(self.projeto_selecionado)
        pessoas = projeto.get("pessoas", []) if projeto else []

        for i, pessoa in enumerate(pessoas):
            tag = "odd" if i % 2 == 0 else "even"
            tree.insert("", "end", values=(
                pessoa.get("nome", "-"),
                pessoa.get("cargo", "-"),
                pessoa.get("etapa", "-"),
                pessoa.get("prazo", "-")
            ), tags=(tag,))

        tree.tag_configure("odd", background="#2c2c2c")
        tree.tag_configure("even", background="#1e1e1e")
        tree.pack(fill="both", expand=True)

    def add_bottom_widgets(self):
        frame_lista = ctk.CTkFrame(self)
        frame_lista.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame_lista, text="Projetos", font=("Roboto", 16)).pack(pady=10)

        self.lista_projetos_frame = ctk.CTkScrollableFrame(frame_lista)
        self.lista_projetos_frame.pack(pady=10, fill="both", expand=True)

        frame_info = ctk.CTkFrame(self)
        frame_info.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame_info, text="Detalhes do Projeto", font=("Roboto", 16)).pack(pady=10)

        self.detalhes_frame = ctk.CTkFrame(master=frame_info)
        self.detalhes_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.treeview_frame = ctk.CTkFrame(self.detalhes_frame)
        self.treeview_frame.pack(fill="both", expand=True)

        self.mostrar_projetos()

    def mostrar_projetos(self):
        for widget in self.lista_projetos_frame.winfo_children():
            widget.destroy()

        projetos = banco.carregar_projetos().get("projetos", [])
        if not projetos:
            ctk.CTkLabel(self.lista_projetos_frame, text="Nenhum projeto encontrado").pack()
            return

        def make_btn_callback(p):
            return lambda: self.mostrar_detalhes_projeto(p)

        for projeto in projetos:
            nome = projeto.get("nome", "Sem Nome")
            id_proj = projeto.get("id", "N/A")
            texto = f"{id_proj} - {nome}"
            ctk.CTkButton(
                self.lista_projetos_frame,
                text=texto,
                command=make_btn_callback(projeto)
            ).pack(pady=2, fill="x")

    def mostrar_detalhes_projeto(self, projeto):
        self.projeto_selecionado = projeto.get("id")

        for widget in self.treeview_frame.winfo_children():
            widget.destroy()

        etapas = projeto.get("etapas", [])
        total = len(etapas)
        concluidas = sum(1 for e in etapas if e['status'] == 'concluído')
        progresso = (concluidas / total) if total > 0 else 0
        self.progress_bar.set(progresso)
        self.progress_label.configure(text=f"{int(progresso * 100)}%")

        for widget in self.detalhes_frame.winfo_children():
            if widget != self.treeview_frame:
                widget.destroy()

        ctk.CTkLabel(self.detalhes_frame, text=f"ID: {projeto.get('id')}", font=("Roboto", 12)).pack()
        ctk.CTkLabel(self.detalhes_frame, text=f"Nome: {projeto.get('nome')}", font=("Roboto", 12)).pack()
        ctk.CTkLabel(self.detalhes_frame, text=f"Descrição: {projeto.get('descricao', '-')}", font=("Roboto", 12)).pack(pady=5)

        colunas = ("Etapa", "Status", "Prazo", "Responsável")
        tree = ttk.Treeview(self.treeview_frame, columns=colunas, show="headings", height=8)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        for i, etapa in enumerate(etapas):
            tag = "odd" if i % 2 == 0 else "even"
            tree.insert("", "end", values=(
                etapa.get("nome", "-"),
                etapa.get("status", "-"),
                etapa.get("prazo", "-"),
                etapa.get("responsavel", "-")
            ), tags=(tag,))

        tree.tag_configure("odd", background="#2c2c2c")
        tree.tag_configure("even", background="#1e1e1e")
        tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.atualizar_pessoas()

    def atualizar_tela(self):
        self.mostrar_projetos()
        if self.projeto_selecionado:
            projeto = banco.carregar_projeto_por_id(self.projeto_selecionado)
            if projeto:
                self.mostrar_detalhes_projeto(projeto)


if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
