import PySimpleGUI as Sg

class TelaLoginAdmin:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Layout da tela de login admin
        layout = [
            [Sg.Push(), Sg.Text('CPF Admin:', size=(15, 1)), Sg.Input(key='cpf_admin', size=(40, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text('Senha Admin:', size=(15, 1)), Sg.Input(key='senha_admin', password_char='*', size=(40, 1)), Sg.Push()],
            [Sg.Push(), Sg.Button('Login', size=(15, 1)), Sg.Push()],
            [Sg.Push(), Sg.Button('Voltar', size=(15, 1)), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window('Tela de Login Admin', layout, size=(600, 300))

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED or evento == 'Voltar':
                self.voltar_para_login_passageiro()
                break
            elif evento == 'Login':
                self.login(valores)

        self.janela.close()

    def login(self, valores):
        cpf = valores['cpf_admin']
        senha = valores['senha_admin']

        sucesso, mensagem = self.controlador.controlador_admin_login.validar_login_admin(cpf, senha)
        if sucesso:
            Sg.popup("Sucesso", mensagem)
            self.abrir_tela_principal_admin()
        else:
            Sg.popup_error("Erro", mensagem)

    def abrir_tela_principal_admin(self):
        self.janela.close()
        from view.ViewAdmin import TelaAdmin
        TelaAdmin(self.controlador).abrir()

    def voltar_para_login_passageiro(self):
        self.janela.close()
        from view.ViewLogin import TelaLogin
        TelaLogin(self.controlador).abrir()
