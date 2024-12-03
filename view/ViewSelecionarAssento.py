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
                linha.append(Sg.Button(assento, size=(5, 2), button_color=("white", cor), key=assento))
            layout.append(linha)

        layout.append([Sg.Button("Confirmar"), Sg.Button("Cancelar")])
        self.janela = Sg.Window("Selecionar Assento", layout)

    def abrir(self):
        assento_selecionado = None  # Variável para armazenar o assento selecionado

        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED or evento == "Cancelar":
                self.retornar_tela_reservas()
                break

            # Verificar se um assento foi clicado
            if isinstance(evento, str) and evento.isalnum():  # Verifica se o evento é um assento
                assento_selecionado = evento  # Armazena o assento selecionado
                # Atualiza a cor do botão selecionado para azul
                for elemento in self.janela.key_dict.values():
                    if hasattr(elemento, "ButtonColor") and elemento.Key == assento_selecionado:
                        elemento.update(button_color=("white", "blue"))
                    elif hasattr(elemento, "ButtonColor"):
                        # Reseta as cores dos outros botões para verde se forem disponíveis
                        elemento.update(button_color=("white", "green"))

            # Quando confirmar, valida o assento selecionado
            if evento == "Confirmar":
                if not assento_selecionado:
                    Sg.popup_error("Nenhum assento selecionado. Selecione um assento antes de confirmar.")
                else:
                    # Atualizar a reserva com o assento selecionado
                    sucesso, mensagem = self.controlador.controlador_reserva.atualizar_assento(self.reserva.cod,
                                                                                               assento_selecionado)
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
