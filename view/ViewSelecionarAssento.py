import PySimpleGUI as Sg

class ViewSelecionarAssento:
    def __init__(self, controlador, reserva):
        self.controlador = controlador
        self.reserva = reserva
        self.janela = None
        self.fileiras_disponiveis = []
        self.assentos_disponiveis = []
        self.criar_janela()

    def criar_janela(self):
        voo = self.controlador.controlador_voo.buscar_voo_por_codigo(self.reserva.voo)
        self.fileiras_disponiveis = self.controlador.controlador_reserva.listar_fileiras_disponiveis(voo)
        layout = [
            [Sg.Text("Selecionar Assento")],
            [Sg.Text("Fileira"), Sg.Combo(self.fileiras_disponiveis, key="fileira", enable_events=True)],
            [Sg.Text("Assento"), Sg.Combo([], key="assento")],
            [Sg.Button("Confirmar", size=(10, 1)), Sg.Button("Cancelar", size=(10, 1))]
        ]
        self.janela = Sg.Window("Selecionar Assento", layout)

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED or evento == "Cancelar":
                self.retornar_tela_reservas()
                break

            if evento == "fileira":
                fileira_selecionada = valores["fileira"]
                self.assentos_disponiveis = self.controlador.controlador_reserva.listar_assentos_disponiveis(self.reserva.voo, fileira_selecionada)
                self.janela["assento"].update(values=self.assentos_disponiveis)

            if evento == "Confirmar":
                assento_selecionado = valores["assento"]
                if assento_selecionado:
                    sucesso, mensagem = self.controlador.controlador_reserva.atualizar_assento(self.reserva.cod, assento_selecionado)
                    if sucesso:
                        Sg.popup("Assento atualizado com sucesso!")
                        self.retornar_tela_reservas()
                        break
                    else:
                        Sg.popup_error("Erro", mensagem)

    def retornar_tela_reservas(self):
        self.janela.close()
        from view.ViewMinhasReservas import TelaMinhasReservas
        TelaMinhasReservas(self.controlador).abrir()
