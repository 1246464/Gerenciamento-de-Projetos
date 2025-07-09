import json
import os
import customtkinter as ctk
from tkinter import messagebox, simpledialog

ARQUIVO_PROJETOS = "dados_projetos.json"

# -----------------------
# Funções de persistência
# -----------------------

def inicializar_banco():
    if not os.path.exists(ARQUIVO_PROJETOS):
        with open(ARQUIVO_PROJETOS, "w") as f:
            json.dump({"projetos": []}, f, indent=4)

def carregar_projetos():
    inicializar_banco()
    try:
        with open(ARQUIVO_PROJETOS, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"projetos": []}

def salvar_projetos(dados):
    try:
        with open(ARQUIVO_PROJETOS, "w") as f:
            json.dump(dados, f, indent=4)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")

# -----------------------
# Utilitários
# -----------------------

def gerar_novo_id(dados):
    if not dados["projetos"]:
        return 1
    return max(p.get("id", 0) for p in dados["projetos"]) + 1

def carregar_projeto_por_id(id_projeto):
    dados = carregar_projetos()
    for projeto in dados["projetos"]:
        if projeto.get("id") == id_projeto:
            return projeto
    return None

def criar_label_entry(janela, texto):
    ctk.CTkLabel(janela, text=texto).pack(pady=(10, 0))
    entrada = ctk.CTkEntry(janela)
    entrada.pack()
    return entrada

# -----------------------
# Interface - Projetos
# -----------------------

def adicionar_projeto(janela_pai, callback=None):
    janela = ctk.CTkToplevel(janela_pai)
    janela.title('Adicionar Projeto')
    janela.geometry('400x300')

    entry_nome = criar_label_entry(janela, 'Nome do Projeto:')
    entry_desc = criar_label_entry(janela, 'Descrição:')

    def salvar():
        nome = entry_nome.get().strip()
        descricao = entry_desc.get().strip()

        if not nome:
            messagebox.showwarning("Aviso", "O nome do projeto é obrigatório!")
            return

        dados = carregar_projetos()
        novo_projeto = {
            "id": gerar_novo_id(dados),
            "nome": nome,
            "descricao": descricao,
            "pessoas": [],
            "etapas": []
        }
        dados["projetos"].append(novo_projeto)
        salvar_projetos(dados)
        messagebox.showinfo("Sucesso", f"Projeto '{nome}' adicionado com sucesso!")
        janela.destroy()
        if callback:
            callback()

    ctk.CTkButton(janela, text='Salvar Projeto', command=salvar).pack(pady=20)

def editar_projeto(janela_pai, id_projeto, callback=None):
    projeto = carregar_projeto_por_id(id_projeto)
    if not projeto:
        messagebox.showerror("Erro", "Projeto não encontrado.")
        return

    janela = ctk.CTkToplevel(janela_pai)
    janela.title('Editar Projeto')
    janela.geometry('400x300')

    entry_nome = criar_label_entry(janela, 'Nome do Projeto:')
    entry_nome.insert(0, projeto.get("nome", ""))

    entry_desc = criar_label_entry(janela, 'Descrição:')
    entry_desc.insert(0, projeto.get("descricao", ""))

    def salvar():
        projeto["nome"] = entry_nome.get().strip()
        projeto["descricao"] = entry_desc.get().strip()
        dados = carregar_projetos()
        for i, p in enumerate(dados["projetos"]):
            if p["id"] == id_projeto:
                dados["projetos"][i] = projeto
                break
        salvar_projetos(dados)
        messagebox.showinfo("Sucesso", "Projeto atualizado com sucesso!")
        janela.destroy()
        if callback:
            callback()

    ctk.CTkButton(janela, text='Salvar Alterações', command=salvar).pack(pady=20)

def excluir_projeto(janela_pai, id_projeto, callback=None):
    resposta = messagebox.askyesno("Confirmar", "Deseja excluir este projeto?")
    if resposta:
        dados = carregar_projetos()
        dados["projetos"] = [p for p in dados["projetos"] if p.get("id") != id_projeto]
        salvar_projetos(dados)
        messagebox.showinfo("Sucesso", "Projeto excluído com sucesso!")
        if callback:
            callback()

def definir_prazo_geral(janela_pai, id_projeto, callback=None):
    projeto = carregar_projeto_por_id(id_projeto)
    if not projeto:
        messagebox.showerror("Erro", "Projeto não encontrado.")
        return
    prazo = simpledialog.askstring("Prazo", "Digite o prazo geral do projeto:")
    if prazo:
        projeto["prazo"] = prazo
        dados = carregar_projetos()
        for i, p in enumerate(dados["projetos"]):
            if p["id"] == id_projeto:
                dados["projetos"][i] = projeto
                break
        salvar_projetos(dados)
        if callback:
            callback()

# -----------------------
# Interface - Etapas
# -----------------------

def adicionar_etapa_com_dados(id_projeto, nome, status, prazo, responsavel):
    dados = carregar_projetos()
    for projeto in dados["projetos"]:
        if projeto.get("id") == id_projeto:
            projeto.setdefault("etapas", []).append({
                "nome": nome,
                "status": status,
                "prazo": prazo,
                "responsavel": responsavel
            })
            salvar_projetos(dados)
            return True
    return False

def janela_adicionar_etapa(janela_pai, callback=None):
    janela = ctk.CTkToplevel(janela_pai)
    janela.title("Adicionar Etapa")
    janela.geometry("400x400")

    entry_id = criar_label_entry(janela, "ID do Projeto:")
    entry_nome = criar_label_entry(janela, "Nome da Etapa:")

    ctk.CTkLabel(janela, text="Status:").pack(pady=(10, 0))
    option_status = ctk.CTkOptionMenu(janela, values=["pendente", "em andamento", "concluído"])
    option_status.set("pendente")
    option_status.pack()

    entry_prazo = criar_label_entry(janela, "Prazo (DD-MM-AAAA):")
    entry_responsavel = criar_label_entry(janela, "Responsável:")

    def salvar():
        try:
            id_projeto = int(entry_id.get())
        except ValueError:
            messagebox.showerror("Erro", "ID do projeto deve ser um número.")
            return

        nome = entry_nome.get().strip()
        status = option_status.get()
        prazo = entry_prazo.get().strip()
        responsavel = entry_responsavel.get().strip()

        if not nome:
            messagebox.showerror("Erro", "Nome da etapa é obrigatório.")
            return

        sucesso = adicionar_etapa_com_dados(id_projeto, nome, status, prazo, responsavel)
        if sucesso:
            messagebox.showinfo("Sucesso", "Etapa adicionada com sucesso!")
            janela.destroy()
            if callback:
                callback()
        else:
            messagebox.showerror("Erro", "Projeto não encontrado.")

    ctk.CTkButton(janela, text="Salvar Etapa", command=salvar).pack(pady=20)

# -----------------------
# Participantes (completo)
# -----------------------

def adicionar_participante(janela, id_projeto, callback=None):
    projeto = carregar_projeto_por_id(id_projeto)
    if not projeto:
        messagebox.showerror("Erro", "Projeto não encontrado.")
        return

    win = ctk.CTkToplevel(janela)
    win.title("Adicionar Participante")
    win.geometry("400x350")

    entry_nome = criar_label_entry(win, "Nome:")
    entry_cargo = criar_label_entry(win, "Cargo:")
    entry_etapa = criar_label_entry(win, "Etapa:")
    entry_prazo = criar_label_entry(win, "Prazo:")

    def salvar():
        pessoa = {
            "nome": entry_nome.get().strip(),
            "cargo": entry_cargo.get().strip(),
            "etapa": entry_etapa.get().strip(),
            "prazo": entry_prazo.get().strip()
        }
        if not pessoa["nome"]:
            messagebox.showwarning("Aviso", "Nome é obrigatório.")
            return

        projeto["pessoas"].append(pessoa)
        dados = carregar_projetos()
        for i, p in enumerate(dados["projetos"]):
            if p["id"] == id_projeto:
                dados["projetos"][i] = projeto
                break
        salvar_projetos(dados)
        messagebox.showinfo("Sucesso", "Participante adicionado!")
        win.destroy()
        if callback:
            callback()

    ctk.CTkButton(win, text="Salvar Participante", command=salvar).pack(pady=20)

def editar_participante(janela, id_projeto, callback=None):
    projeto = carregar_projeto_por_id(id_projeto)
    if not projeto or not projeto.get("pessoas"):
        messagebox.showwarning("Aviso", "Nenhum participante encontrado.")
        return

    nomes = [p["nome"] for p in projeto["pessoas"]]
    nome_escolhido = simpledialog.askstring("Editar Participante", f"Digite o nome do participante:\n{', '.join(nomes)}")
    if not nome_escolhido:
        return

    participante = next((p for p in projeto["pessoas"] if p["nome"] == nome_escolhido.strip()), None)
    if not participante:
        messagebox.showerror("Erro", "Participante não encontrado.")
        return

    win = ctk.CTkToplevel(janela)
    win.title("Editar Participante")
    win.geometry("400x350")

    entry_nome = criar_label_entry(win, "Nome:")
    entry_nome.insert(0, participante["nome"])
    entry_cargo = criar_label_entry(win, "Cargo:")
    entry_cargo.insert(0, participante["cargo"])
    entry_etapa = criar_label_entry(win, "Etapa:")
    entry_etapa.insert(0, participante["etapa"])
    entry_prazo = criar_label_entry(win, "Prazo:")
    entry_prazo.insert(0, participante["prazo"])

    def salvar():
        participante["nome"] = entry_nome.get().strip()
        participante["cargo"] = entry_cargo.get().strip()
        participante["etapa"] = entry_etapa.get().strip()
        participante["prazo"] = entry_prazo.get().strip()
        salvar_projetos(carregar_projetos())
        messagebox.showinfo("Sucesso", "Participante atualizado!")
        win.destroy()
        if callback:
            callback()

    ctk.CTkButton(win, text="Salvar Alterações", command=salvar).pack(pady=20)

def remover_participante(janela, id_projeto, callback=None):
    projeto = carregar_projeto_por_id(id_projeto)
    if not projeto or not projeto.get("pessoas"):
        messagebox.showwarning("Aviso", "Nenhum participante para remover.")
        return

    nomes = [p["nome"] for p in projeto["pessoas"]]
    nome_escolhido = simpledialog.askstring("Remover Participante", f"Digite o nome do participante para remover:\n{', '.join(nomes)}")
    if not nome_escolhido:
        return

    projeto["pessoas"] = [p for p in projeto["pessoas"] if p["nome"] != nome_escolhido.strip()]
    dados = carregar_projetos()
    for i, p in enumerate(dados["projetos"]):
        if p["id"] == id_projeto:
            dados["projetos"][i] = projeto
            break
    salvar_projetos(dados)
    messagebox.showinfo("Sucesso", "Participante removido.")
    if callback:
        callback()
