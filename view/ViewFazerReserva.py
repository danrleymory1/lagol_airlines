import sys
import PySimpleGUI as Sg

class TelaFazerReserva:
    def __init__(self, controlador, voo_cod):
        self.controlador = controlador
        self.janela = None
        self.__voo_cod = voo_cod
        self.__voo = self.controlador.controlador_voo.buscar_por_cod(self.__voo_cod)
        self.criar_janela()
        


    def criar_janela(self):

        dados_voo_layout = [
            [Sg.Text(f"COD: {self.__voo.cod}", size=(15, 1)), Sg.Text(f"Origem: {self.__voo.origem}", size=(20, 1)), Sg.Text(f"Data: {self.__voo.data}", size=(15, 1))],
            [Sg.Text(f"Avião: {self.__voo.aeronave}", size=(15, 1)), Sg.Text(f"Destino: {self.__voo.destino}", size=(20, 1))],
        ]

        dados_passageiro_layout = [
            [Sg.Text("O passageiro é o usuario?")],
            [Sg.Radio("Sim", "passageiro_usuario", key="usuario_sim", enable_events=True), 
            Sg.Radio("Não", "passageiro_usuario", key="usuario_nao", enable_events=True)],
            [Sg.Text("Caso não:")],
            [Sg.Text("Nome                      CPF                      Data de nascimento")],
            [Sg.InputText(key="nome", size=(15, 1), tooltip="Nome", disabled=True,), 
            Sg.InputText(key="cpf", size=(15, 1), tooltip="CPF", disabled=True), 
            Sg.InputText(key="nascimento", size=(15, 1), tooltip="Nascimento", disabled=True)],
        ]

        layout = [
            [Sg.Frame("Dados do voo", dados_voo_layout)],
            [Sg.Frame("Dados do passageiro", dados_passageiro_layout)],
            [Sg.Button("Voltar", size=(10, 1)), Sg.Push(), Sg.Button("Reservar", size=(10, 1))]
        ]

        self.janela = Sg.Window("Reserva de Voo", layout)

    def abrir(self):
        while True:
            event, values = self.janela.read()
            
            if event == "Voltar":
                self.retornar_tela_voos()
                break

            elif event == Sg.WINDOW_CLOSED:
                sys.exit()
            
            # Habilita/desabilita os campos de texto dependendo da seleção dos radio buttons
            if event == "usuario_sim":
                self.janela["nome"].update(disabled=True)
                self.janela["cpf"].update(disabled=True)
                self.janela["nascimento"].update(disabled=True)
            elif event == "usuario_nao":
                self.janela["nome"].update(disabled=False)
                self.janela["cpf"].update(disabled=False)
                self.janela["nascimento"].update(disabled=False)
            
            if event == "Reservar":
            
                if values["usuario_nao"] and (not values["nome"] or not values["cpf"] or not values["nascimento"]):
                    Sg.popup("Erro", "Preencha os dados do passageiro.")
                else:
                    Sg.popup("Reserva Confirmada", "Sua reserva foi realizada com sucesso!")

    def retornar_tela_voos(self):
            self.janela.close()
            from view.ViewVerVoos import TelaVerVoos
            TelaVerVoos(self.controlador).abrir()


