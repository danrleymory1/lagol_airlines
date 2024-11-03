import PySimpleGUI as Sg
from datetime import datetime

class ViewAdicionarVoo:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        layout = [
            [Sg.Text('Código do Voo'), Sg.Input(key='cod')],
            [Sg.Text('Aeronave'), Sg.Input(key='aeronave')],
            [Sg.Text('Assentos'), Sg.Input(key='assentos')],
            [Sg.Text('Origem'), Sg.Input(key='origem')],
            [Sg.Text('Destino'), Sg.Input(key='destino')],
            [Sg.Text('Data (dd/mm/yyyy)'), Sg.Input(key='data')],
            [Sg.Text('Piloto'), Sg.Input(key='piloto')],
            [Sg.Text('Aeromoça'), Sg.Input(key='aeromoca')],
            [Sg.Button('Adicionar', size=(10, 1)), Sg.Button('Cancelar', size=(10, 1))]
        ]
        self.janela = Sg.Window('Adicionar Voo', layout)

    def validar_dados(self, valores):
        try:
            # Validar campos obrigatórios
            if not valores['cod'] or not valores['aeronave'] or not valores['assentos']:
                return False, "Informação inválida, tente novamente."

            # Verificar se 'assentos' é um número
            assentos = int(valores['assentos'])
            if assentos <= 0:
                return False, "Informação inválida, tente novamente."

            # Validar a data
            data = datetime.strptime(valores['data'], '%d/%m/%Y')
            
            return True, "Dados válidos", data
        except ValueError:
            return False, "Informação inválida, tente novamente."
        except Exception as e:
            return False, "Informação inválida, tente novamente."

    def abrir(self):
        while True:
            evento, valores = self.janela.read()
            if evento == Sg.WINDOW_CLOSED or evento == 'Cancelar':
                break
            elif evento == 'Adicionar':
                # Validação dos dados
                sucesso, mensagem, data = self.validar_dados(valores)
                if not sucesso:
                    Sg.popup(mensagem)
                    continue

                # Cadastro de voo no sistema
                sucesso, mensagem = self.controlador.controlador_voo.cadastrar_voo(
                    valores['cod'], valores['aeronave'], int(valores['assentos']), valores['origem'],
                    valores['destino'], data, valores['piloto'], valores['aeromoca']
                )

                # Exibir a mensagem de sucesso conforme o diagrama
                if sucesso:
                    Sg.popup("Cadastro de voo realizado com sucesso")
                    break
                else:
                    Sg.popup("Informação inválida, tente novamente")

        self.janela.close()
