import PySimpleGUI as Sg
from datetime import datetime

class ViewAlterarVoo:
    def __init__(self, controlador, voo):
        self.controlador = controlador
        self.voo = voo
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        layout = [
            [Sg.Text('Origem'), Sg.Input(default_text=self.voo.origem, key='origem')],
            [Sg.Text('Destino'), Sg.Input(default_text=self.voo.destino, key='destino')],
            [Sg.Text('Data (dd/mm/yyyy)'), Sg.Input(default_text=self.voo.data.strftime('%d/%m/%Y'), key='data')],
            [Sg.Button('Salvar', size=(10, 1)), Sg.Button('Cancelar', size=(10, 1))]
        ]
        self.janela = Sg.Window('Alterar Voo', layout)

    def validar_dados(self, valores):
        try:
            # Validar data
            nova_data = datetime.strptime(valores['data'], '%d/%m/%Y')
            return True, "Dados válidos", nova_data
        except ValueError:
            return False, "Informação inválida, por favor, tente novamente."
    
    def abrir(self):
        while True:
            evento, valores = self.janela.read()
            if evento == Sg.WINDOW_CLOSED or evento == 'Cancelar':
                break
            elif evento == 'Salvar':
                # Validação dos dados
                sucesso, mensagem, nova_data = self.validar_dados(valores)
                if not sucesso:
                    Sg.popup(mensagem)
                    continue

                # Realizar alteração de voo
                sucesso, mensagem = self.controlador.controlador_voo.alterar_voo(
                    self.voo.cod, nova_origem=valores['origem'], novo_destino=valores['destino'], nova_data=nova_data
                )

                # Exibir a mensagem de acordo com o resultado da operação
                if sucesso:
                    Sg.popup("Voo alterado com sucesso")
                    break
                else:
                    Sg.popup("Informação inválida, por favor, tente novamente")

        self.janela.close()
