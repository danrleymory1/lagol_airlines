import sys
import PySimpleGUI as Sg
from PySimpleGUI import popup


class TelaVerVoos:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Cabeçalho e layout inicial
        layout = [
            [Sg.Button('Retornar', size=(10, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text('Ver voos', font=("Arial", 14)), Sg.Push()],
            [Sg.Column([[Sg.Text(f"{'Origem':<20} {'Destino':<20} {'Data':<15} {'Horario'}")]])],  # Cabeçalho da lista
            [Sg.Column(self.carregar_voos(), scrollable=True, vertical_scroll_only=True, size=(500, 300))],
            
        ]

        # Cria a janela
        self.janela = Sg.Window('Ver voos', layout, size=(600, 500))

    def carregar_voos(self):
        voos = self.controlador.controlador_voo.buscar_todos_voos()
        if voos:
            voos_layout = []
            for voo in voos:
                voos_layout.append([
                    Sg.Text(f"{voo.origem:<20} {voo.destino:<20} {voo.data:<15} {voo.horario_decolagem:<8}"),
                    Sg.Push(),
                    Sg.Button('Escolher', key=f'escolher_{voo.cod}', size=(10, 1)),
                    #Sg.Button('Deletar', key=f'deletar_{voo.cod}', size=(10, 1)) 
                ])
            return voos_layout
        else:
            Sg.popup("Informação", "Nenhum voo cadastrado.")
            return [[Sg.Text("Nenhum voo cadastrado.")]]

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == 'Retornar':
                self.retornar_tela_cliente()
                break
            elif evento == Sg.WINDOW_CLOSED:
                sys.exit()
            elif evento.startswith('escolher_'):
                voo_cod = evento.split('_')[1]
                self.abrir_tela_fazer_reserva()

        self.janela.close()

    def abrir_tela_fazer_reserva(self):
        self.janela.close()

        from view.ViewFazerReserva import TelaFazerReserva
        TelaFazerReserva(self.controlador).abrir()


    def retornar_tela_cliente(self):
        self.janela.close()
        from view.ViewCliente import TelaCliente
        TelaCliente(self.controlador).abrir()
