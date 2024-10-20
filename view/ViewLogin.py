import PySimpleGUI as Sg
from view.ViewCadastroCliente import TelaCadastroCliente


class TelaLogin:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Layout da tela de login
        layout = [
            [Sg.Push(), Sg.Button('Login Admin', key='admin_login', size=(10, 1))],
            [Sg.Push(), Sg.Text('CPF:', size=(10, 1)), Sg.Input(key='cpf'), Sg.Push()],
            [Sg.Push(), Sg.Text('Senha:', size=(10, 1)), Sg.Input(key='senha', password_char='*'), Sg.Push()],
            [Sg.Push(), Sg.Button('Login', size=(10, 1)), Sg.Push()],
            [Sg.Push(), Sg.Button('Cadastrar', size=(10, 1)), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window('Tela de Login', layout, size=(600, 500))

    def abrir(self):
        # Loop de eventos da interface
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED:
                break
            elif evento == 'Login':
                self.login(valores['cpf'], valores['senha'])
            elif evento == 'Cadastrar':
                self.abrir_cadastro()
            elif evento == 'admin_login':
                self.abrir_login_admin()

        self.janela.close()

    def login(self, cpf, senha):
        sucesso, mensagem = self.controlador.controlador_cliente.validar_login(cpf, senha)
        if sucesso:
            Sg.popup("Sucesso", mensagem)
            self.janela.close()
            from view.ViewCliente import TelaCliente
            TelaCliente(self.controlador).abrir()
        else:
            Sg.popup_error("Erro", mensagem)

    def abrir_cadastro(self):
        self.janela.close()
        TelaCadastroCliente(self.controlador).abrir()

    def abrir_login_admin(self):
        from view.ViewAdminLogin import TelaLoginAdmin
        self.janela.close()
        TelaLoginAdmin(self.controlador).abrir()
