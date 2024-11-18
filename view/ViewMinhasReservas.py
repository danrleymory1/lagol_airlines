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

        if not self._reservas:
            layout.append([Sg.Text("Nenhuma reserva encontrada.")])
            layout.append([Sg.Button("Voltar", size=(10, 1))])
            self.janela = Sg.Window("Minhas Reservas", layout)
            return

        # Para cada reserva, criamos um "card" com as informações e botões
        for i, reserva in enumerate(self._reservas):

            voo = self.controlador.controlador_voo.buscar_voo_por_codigo(reserva.voo)

            layout += [
                [Sg.Text(f"Voo: {reserva.voo}   Origem: {voo.origem}   Passageiro: {reserva.passageiro}", size=(50, 1))],
                [Sg.Text(f"Data: {voo.data}   Destino: {voo.destino}", size=(50, 1))],
                [Sg.Text(f"Bagagens: {reserva.quant_bagagem}   Assento: {reserva.assento}", size=(50, 1))],
                [
                    Sg.Button("Adicionar bagagem", key=f"add_bagagem_{i}", size=(15, 1)),
                    Sg.Button("Alterar assento", key=f"alterar_assento_{i}", size=(15, 1)),
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
                    self.ir_para_tela_selecionar_assento(self._reservas[i], i)
                elif event == f"ver_ticket_{i}":
                    self.ir_para_tela_ticket(self._reservas[i].cod)
                elif event == f"remarcar_voo_{i}":
                    Sg.popup(f"Função não implementada ainda")
                elif event == f"cancelar_{i}":
                    self.cancelar_voo(self._reservas[i].cod)

    def ir_para_tela_cliente(self):
        self.janela.close()
        from view.ViewCliente import TelaCliente
        TelaCliente(self.controlador).abrir()

    def ir_para_tela_ticket(self, reserva_cod):
        self.janela.close()
        from view.ViewVerTicket import TelaVerTicket
        TelaVerTicket(self.controlador, reserva_cod).abrir()

    def ir_para_tela_selecionar_assento(self, reserva, index):
        voo = self.controlador.controlador_voo.buscar_voo_por_codigo(reserva.voo)
        if isinstance(voo, str):  # Garantir que o voo seja um objeto correto
            Sg.popup_error("Erro ao carregar informações do voo.")
            return

        self.janela.close()
        from view.ViewSelecionarAssento import ViewSelecionarAssento
        ViewSelecionarAssento(self.controlador, reserva).abrir()

    def cancelar_voo(self, reserva_cod):
        print("1")
        res = Sg.popup("Tem certeza que deseja excluir este voo?", title="Excluir Voo",  custom_text=("Confirmar", "Cancelar"))
        if res == "Confirmar":
            try:
                self.controlador.controlador_reserva.deletar_reserva(reserva_cod)
                Sg.popup("Reserva cancelada com sucesso.")
            except Exception as e:
                Sg.popup_error(f"Erro ao cancelar reserva: {e}")

            self.janela.close()
            self.ir_para_tela_cliente()
        else:
            Sg.popup("Sua reserva NÃO foi cancelada!")
            self.janela.close()
            self.criar_janela()

            
