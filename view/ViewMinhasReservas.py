import sys
import PySimpleGUI as Sg


class TelaMinhasReservas:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self._reservas = self.controlador.controlador_reserva.buscar_reservas_por_cliente(self.controlador.controlador_cliente.cliente_logado.cpf)
        self.criar_janela()
        

    def criar_janela(self):
        layout = []

        print(self.controlador.controlador_cliente.cliente_logado.cpf)
        print(self.controlador.controlador_reserva.buscar_reservas_por_cliente(self.controlador.controlador_cliente.cliente_logado.cpf))

        # Para cada reserva, criamos um "card" com as informações e botões
        for i, reserva in enumerate(self._reservas):

            voo = self.controlador.controlador_voo.buscar_voo_por_codigo(reserva.voo)

            layout += [
                [Sg.Text(f"Voo: {reserva.voo}   Origem: {voo.origem}   Passageiro: {reserva.passageiro}", size=(50, 1))],
                [Sg.Text(f"Data: {voo.data}   Destino: {voo.destino}   Bagagens: {reserva.quant_bagagem}   Assento: {reserva.assento}", size=(50, 1))],
                [
                    Sg.Button("Adicionar bagagem", key=f"add_bagagem_{i}", size=(15, 1)),
                    Sg.Button("Alterar assento", key=f"alterar_assento_{i}", size=(15, 1)),
                    Sg.Push(),
                    Sg.Button("Ver Ticket", key=f"ver_ticket_{i}", size=(10, 1)),
                    Sg.Button("Remarcar voo", key=f"remarcar_voo_{i}", size=(15, 1)),
                    Sg.Button("Cancelar", key=f"cancelar_{i}", size=(10, 1)),
                ],
                [Sg.HorizontalSeparator()],
            ]

        layout.append([Sg.Button("Voltar", size=(10, 1))])

        self.janela = Sg.Window("Minhas Reservas", layout)

    def abrir(self):
        while True:
            event, values = self.janela.read()

            if event == "Voltar":
                self.ir_para_tela_cliente()
            elif event == Sg.WINDOW_CLOSED:
                sys.exit()

            # Processar eventos dos botões com base no índice da reserva
            for i in range(len(self._reservas)):
                if event == f"add_bagagem_{i}":
                    Sg.popup(f"Função não implementada ainda")
                elif event == f"alterar_assento_{i}":
                    Sg.popup(f"Função não implementada ainda")
                elif event == f"ver_ticket_{i}":
                    self.ir_para_tela_ticket(self._reservas[i].cod)
                elif event == f"remarcar_voo_{i}":
                    Sg.popup(f"Função não implementada ainda")
                elif event == f"cancelar_{i}":
                    Sg.popup(f"Função não implementada ainda")

    def ir_para_tela_cliente(self):
        self.janela.close()
        from view.ViewCliente import TelaCliente
        TelaCliente(self.controlador).abrir()
    
    def ir_para_tela_ticket(self, reserva_cod):
        self.janela.close()
        from view.ViewVerTicket import TelaVerTicket
        TelaVerTicket(self.controlador, reserva_cod).abrir()

