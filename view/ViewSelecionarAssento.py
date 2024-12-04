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

        # Obter fileiras disponíveis
        fileiras_disponiveis = self.controlador.controlador_reserva.listar_fileiras_disponiveis(voo.cod)

        layout = []
        for fileira in fileiras_disponiveis:
            assentos_disponiveis = self.controlador.controlador_reserva.listar_assentos_disponiveis(voo.cod, fileira)
            linha = []
            for assento in sorted(assentos_disponiveis):
                cor = "green"  # Assento disponível
                for assento_map in voo.assentos:
                    if assento in assento_map and assento_map[assento] is not None:
                        cor = "red"  # Assento ocupado
                linha.append(Sg.Button(assento, size=(2, 1), button_color=("white", cor), key=f"ASSENTO_{assento}"))
            layout.append(linha)

        layout.append([Sg.Button("Confirmar", key="CONFIRMAR"), Sg.Button("Cancelar", key="CANCELAR")])
        self.janela = Sg.Window("Selecionar Assento", layout)

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

                # Atualiza as cores dos botões
                for elemento in self.janela.key_dict.values():
                    if elemento.Key.startswith("ASSENTO_"):
                        if elemento.Key == evento:
                            elemento.update(button_color=("white", "blue"))  # Azul para o selecionado
                        else:
                            elemento.update(button_color=("white", "green"))  # Verde para os outros

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
