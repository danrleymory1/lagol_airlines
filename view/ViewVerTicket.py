import sys
import PySimpleGUI as Sg

class TelaVerTicket:
    def __init__(self, controlador, reserva_cod):
        self.__controlador = controlador
        self.reserva = self.__controlador.controlador_reserva.buscar_reserva_por_cod(reserva_cod)
        
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        
        layout = [
            [Sg.Text(f"Código: {self.reserva.cod}", size=(30, 1))],
            [Sg.Text(f"Voo: {self.reserva.voo}", size=(30, 1))],
            [Sg.Button("Voltar", size=(10, 1))]
        ]

        self.janela = Sg.Window("Ticket de Reserva", layout)

    def abrir(self):
        while True:
            event, _ = self.janela.read()
            if event == "Voltar":
                self.ir_para_tela_minhas_reservas()
            elif event == Sg.WINDOW_CLOSED:
                sys.exit()

       

    def ir_para_tela_minhas_reservas(self):
        self.janela.close()
        from view.ViewMinhasReservas import TelaMinhasReservas
        TelaMinhasReservas(self.__controlador).abrir()