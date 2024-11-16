import PySimpleGUI as Sg

class TelaVerTicket:
    def __init__(self, controlador, reserva):
        self.__controlador = controlador
        self.reserva = self.__controlador.controlador_reserva.buscar_reserva_por_cod(reserva)
        print("aaaaaaaaaaaaaaaa")
        print(self.reserva)
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        
        layout = [
            [Sg.Text(f"Código: {self.reserva['cod']}", size=(30, 1))],
            [Sg.Text(f"Voo: {self.reserva['voo']}", size=(30, 1))],
            [Sg.Text(f"Origem: {self.reserva['origem']}", size=(30, 1))],
            [Sg.Text(f"Destino: {self.reserva['destino']}", size=(30, 1))],
            [Sg.Text(f"Data: {self.reserva['data']}", size=(30, 1))],
            [Sg.Text(f"Assento: {self.reserva['assento']}", size=(30, 1))],
            [Sg.Text(f"Nome: {self.reserva['nome']}", size=(30, 1))],
            [Sg.Text(f"CPF: {self.reserva['cpf']}", size=(30, 1))],
            [Sg.Button("Voltar", size=(10, 1))]
        ]

        self.janela = Sg.Window("Ticket de Reserva", layout)

    def abrir(self):
        while True:
            event, _ = self.janela.read()
            
            if event == "Voltar" or event == Sg.WINDOW_CLOSED:
                break

        self.janela.close()

    def ir_para_tela_minhas_reservas(self):
        self.janela.close()
        from view.ViewMinhasReservas import TelaMinhasReservas