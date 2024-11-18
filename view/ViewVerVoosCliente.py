import sys
import PySimpleGUI as Sg
from PySimpleGUI import popup


class TelaVerVoosCliente:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
    # Cabeçalho e layout inicial
        layout = [
            [Sg.Button('Retornar', size=(10, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text('Ver voos', font=("Arial", 14)), Sg.Push()],
            [
                Sg.Text("Origem", size=(15, 1)),
                Sg.Text("Destino", size=(15, 1)),
                Sg.Text("Data", size=(12, 1)),
                Sg.Text("Horário", size=(10, 1)),
                Sg.Text("", size=(8, 1)),  # Espaço para os botões
            ],  # Cabeçalho com tamanhos fixos
            [Sg.Column(self.carregar_voos(), scrollable=True, vertical_scroll_only=True, size=(550, 300))],
        ]

        # Cria a janela
        self.janela = Sg.Window('Ver voos', layout, size=(600, 500))


    def carregar_voos(self):
        voos = self.controlador.controlador_voo.buscar_todos_voos()
        if voos:
            voos_layout = []
            for voo in voos:
                data = f"{voo.data.day}/{voo.data.month}/{voo.data.year}"
                voos_layout.append([
                    Sg.Text(voo.origem, size=(15, 1)),  # Coluna "Origem"
                    Sg.Text(voo.destino, size=(15, 1)),  # Coluna "Destino"
                    Sg.Text(data, size=(12, 1)),  # Coluna "Data"
                    Sg.Text(voo.horario_decolagem, size=(10, 1)),  # Coluna "Horário"
                    Sg.Button('Escolher', key=f'escolher_{voo.cod}', size=(8, 1)),  # Botão
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
                self.abrir_tela_fazer_reserva(voo_cod)

        self.janela.close()

    def abrir_tela_fazer_reserva(self, voo_cod):
        self.janela.close()

        from view.ViewFazerReserva import TelaFazerReserva
        TelaFazerReserva(self.controlador, voo_cod).abrir()


    def retornar_tela_cliente(self):
        self.janela.close()
        from view.ViewCliente import TelaCliente
        TelaCliente(self.controlador).abrir()