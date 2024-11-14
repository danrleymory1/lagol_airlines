import sys
import PySimpleGUI as Sg

class TelaAdmin:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Layout da tela de admin
        layout = [
            [Sg.Button('Sair', size=(10, 1), key='voltar'), Sg.Push()],
            [Sg.Push(), Sg.Button('Funcionários', size=(30, 2), key='funcionarios'), Sg.Push()],
            [Sg.Push(), Sg.Button('Aviões', size=(30, 2), key='avioes'), Sg.Push()],
            [Sg.Push(), Sg.Button('Voos', size=(30, 2), key='voos'), Sg.Push()],
            [Sg.Push(), Sg.Button('Ver Tickets Emitidos', size=(30, 2), key='tickets'), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window('Tela Admin', layout, size=(600, 400))

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == 'voltar':
                self.voltar_para_login()
                break
            elif evento == Sg.WINDOW_CLOSED:
                sys.exit()
            elif evento == 'funcionarios':
                self.gerenciar_funcionarios()
            elif evento == 'avioes':
                self.gerenciar_avioes()
            elif evento == 'voos':
                self.gerenciar_voos()
            elif evento == 'tickets':
                self.ver_tickets_emitidos()

        self.janela.close()

    def voltar_para_login(self):
        self.janela.close()
        from view.ViewLogin import TelaLogin
        TelaLogin(self.controlador).abrir()

    def gerenciar_funcionarios(self):
        self.janela.close()
        from view.ViewFuncionarios import TelaFuncionarios
        TelaFuncionarios(self.controlador).abrir()

    def gerenciar_avioes(self):
        # Implementação futura
        Sg.popup("Gerenciar Aviões - Em desenvolvimento")

    def gerenciar_voos(self):
        self.janela.close()
        from view.ViewVerVoosAdm import ViewVerVoosAdm
        ViewVerVoosAdm(self.controlador).abrir()

    def ver_tickets_emitidos(self):
        # Implementação futura
        Sg.popup("Ver Tickets Emitidos - Em desenvolvimento")
