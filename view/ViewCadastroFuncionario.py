import sys
import PySimpleGUI as Sg

class TelaCadastroFuncionario:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        layout = [
            [Sg.Push(), Sg.Text("Cadastrar Funcionário", font=("Arial", 14)), Sg.Push()],
            [Sg.Push(), Sg.Text("Nome:"), Sg.Input(key='nome', size=(30, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text("CPF:"), Sg.Input(key='cpf', size=(30, 1)), Sg.Push()],
            [
                Sg.Push(), Sg.Text("Cargo:") ,Sg.Radio('Piloto', "CARGO", key='Piloto', default=True),
                Sg.Radio('Aeromoça', "CARGO", key='Aeromoca'), Sg.Push()
            ],
            [Sg.Push(), Sg.Button('Cadastrar', size=(10, 1)), Sg.Button('Cancelar', size=(10, 1)), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window('Cadastrar Funcionário', layout, size=(400, 300))

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == 'Cancelar':
                self.retornar_tela_funcionario()
                break
            elif evento == Sg.WINDOW_CLOSED:
                sys.exit()
            elif evento == 'Cadastrar':
                self.cadastrar_funcionario(valores)

        self.janela.close()

    def cadastrar_funcionario(self, valores):
        nome = valores['nome']
        cpf = valores['cpf']
        cargo = 'Piloto' if valores['Piloto'] else 'Aeromoca'

        sucesso, mensagem = self.controlador.controlador_funcionario.cadastrar_funcionario(nome, cpf, cargo)

        if sucesso:
            Sg.popup("Sucesso", mensagem)
            self.janela.close()
            from view.ViewFuncionarios import TelaFuncionarios
            TelaFuncionarios(self.controlador).abrir()
        else:
            Sg.popup_error("Erro", mensagem)

    def retornar_tela_funcionario(self):
        self.janela.close()
        from view.ViewFuncionarios import TelaFuncionarios
        TelaFuncionarios(self.controlador).abrir()
