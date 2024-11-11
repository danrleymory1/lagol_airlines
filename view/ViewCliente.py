import sys
import PySimpleGUI as Sg

class TelaCliente:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Obtém os dados do Cliente logado
        cliente = self.controlador.controlador_cliente.cliente_logado
        info_text = f"Nome: {cliente.nome} | CPF: {cliente.cpf} | Data de Nascimento: {cliente.data_nascimento}" if cliente else "Nenhum Cliente logado"

        # Layout da tela do Cliente
        layout = [
            [Sg.Button('Sair', size=(10, 1))],
            [Sg.Text(info_text, size=(50, 1))],
            [Sg.Push(), Sg.Button('Nova Reserva', size=(30, 1)), Sg.Push()],
            [Sg.Push(), Sg.Button('Minhas Reservas', size=(30, 1)), Sg.Push()],
            [Sg.Push(), Sg.Button('Alterar Dados de Usuário', size=(30, 1)), Sg.Push()]

        ]

        # Cria a janela
        self.janela = Sg.Window('Tela do Cliente', layout, size=(600, 400))

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == 'Sair':
                self.voltar_para_login()
                break
            elif evento == Sg.WINDOW_CLOSED:
                sys.exit()
            elif evento == 'Nova Reserva':
                self.nova_reserva()
            elif evento == 'Minhas Reservas':
                self.minhas_reservas()
            elif evento == 'Alterar Dados de Usuário':
                self.alterar_dados()

        self.janela.close()

    def voltar_para_login(self):
        self.janela.close()
        from view.ViewLogin import TelaLogin
        TelaLogin(self.controlador).abrir()

    def nova_reserva(self):
        self.janela.close()
        from view.ViewVerVoosAdm import TelaVerVoos
        TelaVerVoos(self.controlador).abrir()
        

    def minhas_reservas(self):
        # Implementar redirecionamento para minhas reservas
        Sg.popup("Funcionalidade de Minhas Reservas não implementada ainda.")

    def alterar_dados(self):
        self.janela.close()
        from view.ViewAlterarCliente import TelaAlterarCliente
        TelaAlterarCliente(self.controlador).abrir()
