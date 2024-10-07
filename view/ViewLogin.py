import tkinter as tk
from tkinter import messagebox
from view.ViewCadastroPassageiro import TelaCadastroPassageiro

class TelaLogin(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador

        # Configuração da tela
        self.title("Tela de Login")
        self.geometry("800x600")
        self.configure(bg="#f0f4f7")  # Cor de fundo suave

        # Container central para organizar os elementos
        self.container = tk.Frame(self, bg="#f0f4f7")
        self.container.pack(expand=True, padx=20, pady=20)

        # Botão de login do admin no topo esquerdo
        self.admin_login_button = tk.Button(self, text="Login Admin", font=("Arial", 12, "bold"), bg="#FFC107", fg="black",
                                             activebackground="#FFA000", activeforeground="black",
                                             command=self.abrir_login_admin)
        self.admin_login_button.place(x=10, y=10, width=120, height=40)  # Posição e tamanho do botão

        # CPF
        self.cpf_label = tk.Label(self.container, text="CPF:", font=("Arial", 12), bg="#f0f4f7", fg="#333333")
        self.cpf_label.grid(row=0, column=0, pady=(20, 0), sticky="w")
        self.cpf_entry = tk.Entry(self.container, width=40, bg="#ffffff", fg="#333333", borderwidth=2)
        self.cpf_entry.grid(row=0, column=1, pady=(20, 10), padx=10, ipadx=10)

        # Senha
        self.senha_label = tk.Label(self.container, text="Senha:", font=("Arial", 12), bg="#f0f4f7", fg="#333333")
        self.senha_label.grid(row=1, column=0, pady=(20, 0), sticky="w")
        self.senha_entry = tk.Entry(self.container, show="*", width=40, bg="#ffffff", fg="#333333", borderwidth=2)
        self.senha_entry.grid(row=1, column=1, pady=(20, 10), padx=10, ipadx=10)

        # Botão de Login
        self.login_button = tk.Button(self.container, text="Login", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                       activebackground="#45a049", activeforeground="white", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=(10, 5), ipadx=20, ipady=5)

        # Botão de Cadastro
        self.cadastrar_button = tk.Button(self.container, text="Cadastrar", font=("Arial", 12, "bold"), bg="#2196F3",
                                           fg="white", activebackground="#1976D2", activeforeground="white",
                                           command=self.abrir_cadastro)
        self.cadastrar_button.grid(row=3, columnspan=2, pady=(5, 20), ipadx=20, ipady=5)

    def login(self):
        cpf = self.cpf_entry.get()
        senha = self.senha_entry.get()
        sucesso, mensagem = self.controlador.controlador_passageiro.validar_login(cpf, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.destroy()
            from view.ViewPassageiro import TelaPassageiro
            TelaPassageiro(self.controlador)
        else:
            messagebox.showerror("Erro", mensagem)

    def abrir_cadastro(self):
        self.destroy()
        TelaCadastroPassageiro(self.controlador)

    def abrir_login_admin(self):
        from view.ViewAdminLogin import TelaLoginAdmin
        self.destroy()
        TelaLoginAdmin(self.controlador)
