import PySimpleGUI as Sg

class TelaCadastroCliente:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Layout da tela de cadastro
        layout = [
            [Sg.Push(), Sg.Text('Nome:', size=(15, 1)), Sg.Input(key='nome', size=(40, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text('CPF:', size=(15, 1)), Sg.Input(key='cpf', size=(40, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text('Data de Nascimento:', size=(15, 1)), Sg.Input(key='data_nascimento', size=(40, 1)), Sg.Push(), Sg.CalendarButton('Data', target='data_nascimento', format='%d/%m/%Y')],
            [Sg.Push(), Sg.Text('Senha:', size=(15, 1)), Sg.Input(key='senha', password_char='*', size=(40, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text('Confirmar Senha:', size=(15, 1)), Sg.Input(key='confirmar_senha', password_char='*', size=(40, 1)), Sg.Push()],
            [Sg.Push(), Sg.Button('Cadastrar', size=(15, 1)), Sg.Push()],
            [Sg.Push(), Sg.Button('Cancelar', size=(15, 1)), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window('Tela de Cadastro', layout, size=(600, 400))

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED or evento == 'Cancelar':
                break
            elif evento == 'Cadastrar':
                self.cadastrar(valores)

        self.janela.close()

    def cadastrar(self, valores):
        nome = valores['nome']
        cpf = valores['cpf']
        data_nasc = valores['data_nascimento']
        senha = valores['senha']
        confirmar_senha = valores['confirmar_senha']

        sucesso, mensagem = self.controlador.controlador_cliente.cadastrar_cliente(nome, cpf, data_nasc, senha, confirmar_senha)

        if sucesso:
            Sg.popup("Sucesso", mensagem)
            self.janela.close()
            from view.ViewLogin import TelaLogin
            TelaLogin(self.controlador).abrir()
        else:
            Sg.popup_error("Erro", mensagem)
