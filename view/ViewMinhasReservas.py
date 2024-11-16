import PySimpleGUI as Sg


class TelaMinhasReservas:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        layout = []

        # Para cada reserva, criamos um "card" com as informações e botões
        for i, reserva in enumerate(self.controlador.controlador_reserva.buscar_reservas__por_cliente(self.controlador.controlador_cliente.cliente_logado.cpf)):
            layout += [
                [Sg.Text(f"Voo: {reserva['voo']}   Origem: {reserva['origem']}   Passageiro: {reserva['passageiro']}", size=(50, 1))],
                [Sg.Text(f"Data: {reserva['data']}   Destino: {reserva['destino']}   Bagagens: {reserva['bagagens']}   Assento: {reserva['assento']}", size=(50, 1))],
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

            if event == "Voltar" or event == Sg.WINDOW_CLOSED:
                break

            # Processar eventos dos botões com base no índice da reserva
            for i in range(len(self.reservas)):
                if event == f"add_bagagem_{i}":
                    Sg.popup(f"Adicionar bagagem para a reserva {self.reservas[i]['voo']}")
                elif event == f"alterar_assento_{i}":
                    Sg.popup(f"Alterar assento para a reserva {self.reservas[i]['voo']}")
                elif event == f"ver_ticket_{i}":
                    Sg.popup(f"Exibir ticket da reserva {self.reservas[i]['voo']}")
                elif event == f"remarcar_voo_{i}":
                    Sg.popup(f"Remarcar voo {self.reservas[i]['voo']}")
                elif event == f"cancelar_{i}":
                    Sg.popup(f"Cancelar reserva {self.reservas[i]['voo']}")

        self.janela.close()

