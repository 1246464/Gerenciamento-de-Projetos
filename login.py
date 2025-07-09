import json
import os
import customtkinter
from tkinter import simpledialog, messagebox
import subprocess
import sys

# Diretório onde o executável ou script está localizado
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_USUARIOS = os.path.join(BASE_DIR, 'dados_usuarios.json')


class UsuarioManager:
    @staticmethod
    def carregar_dados():
        if os.path.exists(ARQUIVO_USUARIOS):
            try:
                with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Erro", "Arquivo de usuários corrompido.")
        return {}

    @staticmethod
    def salvar_dados(dados):
        with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    @staticmethod
    def validar_entrada(campo, nome):
        valor = simpledialog.askstring(campo, f"Digite seu {nome}:", show='*' if nome == 'senha' else None)
        if not valor or not valor.strip():
            messagebox.showwarning("Aviso", f"{nome.capitalize()} não pode ser vazio.")
            return None
        return valor.strip()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.geometry('500x300')
        self.title("Login - ProjetoX")

        customtkinter.CTkLabel(self, text="Bem-vindo!", font=("Roboto", 20)).pack(pady=10)
        customtkinter.CTkButton(self, text="Login", command=self.login).pack(pady=10)
        customtkinter.CTkButton(self, text="Cadastro", command=self.cadastro).pack(pady=10)

    def cadastro(self):
        dados = UsuarioManager.carregar_dados()
        nome = UsuarioManager.validar_entrada("Cadastro", "nome")
        if not nome:
            return

        if nome in dados:
            messagebox.showinfo("Aviso", "Usuário já existe.")
            return

        senha = UsuarioManager.validar_entrada("Cadastro", "senha")
        if not senha:
            return

        dados[nome] = {"senha": senha}
        UsuarioManager.salvar_dados(dados)
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

    def login(self):
        dados = UsuarioManager.carregar_dados()
        nome = UsuarioManager.validar_entrada("Login", "nome")
        senha = UsuarioManager.validar_entrada("Login", "senha")
        if not nome or not senha:
            return

        if nome in dados and dados[nome]["senha"] == senha:
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.destroy()

            caminho_dashboard = os.path.join(BASE_DIR, "tela_inicial.py")
            if os.path.exists(caminho_dashboard):
                subprocess.Popen(["python", caminho_dashboard])
            else:
                messagebox.showerror("Erro", "Arquivo 'tela_inicial.py' não encontrado.")
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
