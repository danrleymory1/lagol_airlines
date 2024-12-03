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
        assentos_layout = []

        # Renderizar fileiras e assentos com cores
        for fileira in range(1, self.controlador.controlador_reserva.listar_fileiras_disponiveis(voo)):
            linha = []
            for coluna in range(voo.aeronave.assentos_por_fileira):
                assento = f"{fileira}{chr(65 + coluna)}"
                ocupado = any(assento in a and a[assento] is not None for a in voo.assentos)
                cor = "red" if ocupado else "green"
                if self.reserva.assento == assento:
                    cor = "blue"
                linha.append(Sg.Button(assento, size=(5, 2), button_color=("white", cor), key=assento))
            assentos_layout.append(linha)

        layout = [
            [Sg.Text(f"Voo: {self.reserva.voo}   Passageiro: {self.reserva.passageiro}")],
            *assentos_layout,
            [Sg.Button("Confirmar"), Sg.Button("Cancelar")]
        ]
        self.janela = Sg.Window("Selecionar Assento", layout)

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED or evento == "Cancelar":
                self.retornar_tela_reservas()
                break

            # Detectar clique em um assento
            if evento in [f"{fileira}{chr(65 + coluna)}" for fileira in
                          range(1, self.controlador.controlador_reserva.listar_fileiras_disponiveis(self.reserva.voo))
                          for coluna in range(self.reserva.voo.aeronave.assentos_por_fileira)]:
                self.assento_selecionado = evento

                # Atualizar cores dos botões (azul para selecionado, vermelho para ocupados, verde para livres)
                for btn in self.janela.AllKeysDict.values():
                    if isinstance(btn, Sg.Button) and btn.get_text() == self.assento_selecionado:
                        btn.update(button_color=("white", "blue"))
                    elif isinstance(btn, Sg.Button):
                        ocupado = any(
                            btn.get_text() in a and a[btn.get_text()] is not None for a in self.reserva.voo.assentos)
                        cor = "red" if ocupado else "green"
                        btn.update(button_color=("white", cor))

            if evento == "Confirmar":
                if hasattr(self, "assento_selecionado") and self.assento_selecionado:
                    sucesso, mensagem = self.controlador.controlador_reserva.atualizar_assento(self.reserva.cod,
                                                                                               self.assento_selecionado)
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
