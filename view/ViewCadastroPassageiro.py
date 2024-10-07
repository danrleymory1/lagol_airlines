import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox

class TelaCadastroPassageiro(tk.Toplevel):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Tela de Cadastro")
        self.geometry("800x600")
        self.configure(bg="#f0f4f7")  # Cor de fundo suave

        # Container para centralizar os elementos
        self.container = tk.Frame(self, bg="#f0f4f7")
        self.container.pack(expand=True, padx=20, pady=20)

        # Nome
        self.nome_label = tk.Label(self.container, text="Nome:", font=("Arial", 12), bg="#f0f4f7", fg="#333333")
        self.nome_label.grid(row=0, column=0, sticky="w", pady=10)
        self.nome_entry = tk.Entry(self.container, width=50, bg="#ffffff", fg="#333333", borderwidth=2)
        self.nome_entry.grid(row=0, column=1, pady=10, ipadx=10)

        # CPF
        self.cpf_label = tk.Label(self.container, text="CPF:", font=("Arial", 12), bg="#f0f4f7", fg="#333333")
        self.cpf_label.grid(row=1, column=0, sticky="w", pady=10)
        self.cpf_entry = tk.Entry(self.container, width=50, bg="#ffffff", fg="#333333", borderwidth=2)
        self.cpf_entry.grid(row=1, column=1, pady=10, ipadx=10)

        # Data de Nascimento (com input maior)
        self.data_nasc_label = tk.Label(self.container, text="Data de Nascimento:", font=("Arial", 12), bg="#f0f4f7", fg="#333333")
        self.data_nasc_label.grid(row=2, column=0, sticky="w", pady=10)
        self.data_nasc_entry = DateEntry(self.container, width=50, background='darkblue', foreground='white', borderwidth=2, year=2000)
        self.data_nasc_entry.grid(row=2, column=1, pady=10, ipadx=10)

        # Senha
        self.senha_label = tk.Label(self.container, text="Senha:", font=("Arial", 12), bg="#f0f4f7", fg="#333333")
        self.senha_label.grid(row=3, column=0, sticky="w", pady=10)
        self.senha_entry = tk.Entry(self.container, show="*", width=50, bg="#ffffff", fg="#333333", borderwidth=2)
        self.senha_entry.grid(row=3, column=1, pady=10, ipadx=10)

        # Confirmar Senha
        self.confirmar_senha_label = tk.Label(self.container, text="Confirmar Senha:", font=("Arial", 12), bg="#f0f4f7", fg="#333333")
        self.confirmar_senha_label.grid(row=4, column=0, sticky="w", pady=10)
        self.confirmar_senha_entry = tk.Entry(self.container, show="*", width=50, bg="#ffffff", fg="#333333", borderwidth=2)
        self.confirmar_senha_entry.grid(row=4, column=1, pady=10, ipadx=10)

        # Botão Cadastrar
        self.cadastrar_button = tk.Button(self.container, text="Cadastrar", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white", command=self.cadastrar)
        self.cadastrar_button.grid(row=5, columnspan=2, pady=20, ipadx=20, ipady=5)

        # Botão Login (para retornar à tela de login)
        self.login_button = tk.Button(self.container, text="Voltar ao Login", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", activebackground="#1976D2", activeforeground="white", command=self.voltar_login)
        self.login_button.grid(row=6, columnspan=2, pady=10, ipadx=20, ipady=5)

    def cadastrar(self):
        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()
        data_nasc = self.data_nasc_entry.get_date()
        senha = self.senha_entry.get()
        confirmar_senha = self.confirmar_senha_entry.get()

        sucesso, mensagem = self.controlador.controlador_passageiro.cadastrar_passageiro(nome, cpf, data_nasc, senha, confirmar_senha)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.destroy()
        else:
            messagebox.showerror("Erro", mensagem)

    def voltar_login(self):
        self.destroy()  # Fecha a tela de cadastro

