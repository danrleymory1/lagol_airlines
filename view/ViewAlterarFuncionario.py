import sys
import PySimpleGUI as Sg

class TelaAlterarFuncionario:
    def __init__(self, controlador, funcionario_cpf):
        self.controlador = controlador
        self.funcionario_cpf = funcionario_cpf
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Layout da tela de alteração
        layout = [
            [Sg.Text("Alterar Funcionário", font=("Arial", 14))],
            [Sg.Push(), Sg.Text("Nome:"), Sg.Input(key='nome', size=(30, 1)), Sg.Push()],
            [Sg.Push(), Sg.Button('Salvar Alterações', size=(15, 1)), Sg.Button('Cancelar', size=(10, 1)), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window('Alterar Funcionário', layout, size=(400, 200))

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == 'Cancelar':
                self.retornar_funcionario()
                break
            elif evento == Sg.WINDOW_CLOSED:
                sys.exit()
            elif evento == 'Salvar Alterações':
                self.alterar_funcionario(valores)

        self.janela.close()

    def alterar_funcionario(self, valores):
        nome = valores['nome']

        sucesso, mensagem = self.controlador.controlador_funcionario.alterar_funcionario(self.funcionario_cpf, nome)

        if sucesso:
            Sg.popup("Sucesso", mensagem)
            self.janela.close()
            from view.ViewFuncionarios import TelaFuncionarios
            TelaFuncionarios(self.controlador).abrir()
        else:
            Sg.popup_error("Erro", mensagem)

    def retornar_funcionario(self):
        self.janela.close()
        from view.ViewFuncionarios import TelaFuncionarios
        TelaFuncionarios(self.controlador).abrir()
