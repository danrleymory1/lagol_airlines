import PySimpleGUI as Sg

class ViewSelecionarAssento:
    def __init__(self, controlador, reserva):
        self.controlador = controlador
        self.reserva = reserva
        self.janela = None
        self.assento_selecionado = None  # Variável para armazenar o assento selecionado
        self.criar_janela()

    def criar_janela(self):
        voo = self.controlador.controlador_voo.buscar_voo_por_codigo(self.reserva.voo)
        if not voo:
            Sg.popup_error("Erro ao carregar informações do voo.")
            return

        # Buscar todas as reservas do voo
        reservas_voo = self.controlador.controlador_reserva.buscar_reservas_por_voo(voo.cod)

        # Determinar o estado dos assentos com base nas reservas
        assentos_ocupados = {r.assento for r in reservas_voo if r.assento is not None}
        assento_atual = self.reserva.assento  # Assento atual desta reserva
        assentos_layout = []

        for fileira in range(1, voo.aeronave.fileiras + 1):
            linha = []
            for coluna in range(voo.aeronave.assentos_por_fileira):
                assento = f"{fileira}{chr(65 + coluna)}"
                if assento in assentos_ocupados and assento != assento_atual:
                    cor = "red"  # Ocupado
                    habilitado = False
                elif assento == assento_atual:
                    cor = "yellow"  # Assento atual
                    habilitado = False
                else:
                    cor = "green"  # Livre
                    habilitado = True
                linha.append(
                    Sg.Button(
                        assento,
                        size=(5, 2),
                        button_color=("black", cor),  # Fonte preta
                        key=f"ASSENTO_{assento}",
                        disabled=not habilitado,
                    )
                )
            assentos_layout.append(linha)

        # Legenda
        legenda = [
            [Sg.Text("Legenda:", font=("Helvetica", 11), text_color="white")],
            [Sg.Text("🟩 Livre", text_color="black", background_color="green", size=(13, 1), justification="center")],
            [Sg.Text("🟥 Ocupado", text_color="black", background_color="red", size=(13, 1), justification="center")],
            [Sg.Text("🟨 Assento Atual", text_color="black", background_color="yellow", size=(13, 1), justification="center")],
            [Sg.Text("🟦 Selecionado", text_color="white", background_color="blue", size=(13, 1), justification="center")],
        ]

        # Scroll para os assentos
        assentos_scroll = Sg.Column(
            [[Sg.Column(assentos_layout, justification="center")]],
            scrollable=True,
            vertical_scroll_only=True,
            size=(300, 380),
            justification="center",
        )

        # Layout centralizado com legenda e botões
        layout = [
            [Sg.Text("Selecionar Assento", font=("Helvetica", 14), justification="center")],
            [assentos_scroll],
            [Sg.Column(legenda, justification="center")],
            [Sg.Button("Confirmar", key="CONFIRMAR"), Sg.Button("Cancelar", key="CANCELAR")],
        ]

        self.janela = Sg.Window(
            "Selecionar Assento",
            layout,
            size=(400, 600),
            element_justification="center",
            finalize=True,
        )

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento in (Sg.WINDOW_CLOSED, "CANCELAR"):
                self.retornar_tela_reservas()
                break

            # Verificar se o evento é de um botão de assento
            if evento.startswith("ASSENTO_"):
                assento = evento.replace("ASSENTO_", "")  # Extrai o nome do assento
                self.assento_selecionado = assento  # Armazena o assento selecionado
                # Atualizar apenas o botão clicado
                for elemento in self.janela.key_dict.values():
                    if elemento.Key.startswith("ASSENTO_"):
                        cor_atual = elemento.ButtonColor[1]
                        if elemento.Key == evento:
                            elemento.update(button_color=("black", "blue"))  # Azul para o selecionado
                        elif cor_atual == "blue":  # Resetar botões azuis que não são o selecionado
                            elemento.update(button_color=("black", "green") if elemento.Key != evento else elemento.ButtonColor)

            # Quando confirmar, valida o assento selecionado
            if evento == "CONFIRMAR":
                if not self.assento_selecionado:
                    Sg.popup_error("Nenhum assento selecionado. Selecione um assento antes de confirmar.")
                else:
                    sucesso, mensagem = self.controlador.controlador_reserva.atualizar_assento(
                        self.reserva.cod, self.assento_selecionado
                    )
                    if sucesso:
                        Sg.popup("Assento atualizado com sucesso!")
                        self.retornar_tela_reservas()
                        break
                    else:
                        Sg.popup_error("Erro ao atualizar assento:", mensagem)

    def retornar_tela_reservas(self):
        self.janela.close()
        from view.ViewMinhasReservas import TelaMinhasReservas
        TelaMinhasReservas(self.controlador).abrir()
