import tkinter as tk
from tkinter import messagebox

class TelaLoginAdmin(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Tela de Login Admin")
        self.geometry("800x600")
        self.configure(bg="#f0f4f7")  # Cor de fundo suave

        # Definindo largura comum para os campos
        campo_largura = 50

        # CPF Admin
        self.cpf_label = tk.Label(self, text="CPF Admin:", font=("Arial", 12), bg="#f0f4f7", fg="#333333")
        self.cpf_label.pack(pady=(20, 0))  # Adiciona espaço acima
        self.cpf_entry = tk.Entry(self, width=campo_largura, bg="#ffffff", fg="#333333", borderwidth=2)
        self.cpf_entry.pack(pady=(0, 10))  # Adiciona espaço abaixo

        # Senha Admin
        self.senha_label = tk.Label(self, text="Senha Admin:", font=("Arial", 12), bg="#f0f4f7", fg="#333333")
        self.senha_label.pack(pady=(20, 0))  # Adiciona espaço acima
        self.senha_entry = tk.Entry(self, show="*", width=campo_largura, bg="#ffffff", fg="#333333", borderwidth=2)
        self.senha_entry.pack(pady=(0, 20))  # Adiciona espaço abaixo

        # Botão Login
        self.login_button = tk.Button(self, text="Login", command=self.login, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white")
        self.login_button.pack(pady=(10, 5))  # Adiciona espaço abaixo

        # Botão Voltar
        self.voltar_button = tk.Button(self, text="Voltar", command=self.voltar_para_login_passageiro, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", activebackground="#1976D2", activeforeground="white")
        self.voltar_button.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)

    def login(self):
        cpf = self.cpf_entry.get()
        senha = self.senha_entry.get()

        sucesso, mensagem = self.controlador.controlador_admin_login.validar_login_admin(cpf, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.abrir_tela_principal_admin()
        else:
            messagebox.showerror("Erro", mensagem)

    def abrir_tela_principal_admin(self):
        self.destroy()
        from view.ViewAdmin import TelaAdmin
        TelaAdmin(self.controlador)

    def voltar_para_login_passageiro(self):
        self.destroy()
        from view.ViewLogin import TelaLogin
        TelaLogin(self.controlador)
