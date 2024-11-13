import PySimpleGUI as Sg
from datetime import datetime

class ViewAdicionarVoo:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Lista de opções para aviões, pilotos, copilotos e aeromoças
        avioes = ["Avião 1", "Avião 2", "Avião 3"]
        pilotos = ["Piloto 1", "Piloto 2"]
        copilotos = ["Copiloto 1", "Copiloto 2"]
        aeromocas = ["Aeromoça 1", "Aeromoça 2", "Aeromoça 3"]

        layout = [
            [Sg.Text('Aeronave'), Sg.Combo(avioes, key='aeronave')],
            [Sg.Text('Origem'), Sg.Input(key='origem')],
            [Sg.Text('Destino'), Sg.Input(key='destino')],
            [Sg.Text('Data (dd/mm/yyyy)'), Sg.Input(key='data')],
            [Sg.Text('Hora de Decolagem (hh:mm)'), Sg.Input(key='hora')],
            [Sg.Text('Piloto'), Sg.Combo(pilotos, key='piloto')],
            [Sg.Text('Copiloto'), Sg.Combo(copilotos, key='copiloto')],
            [Sg.Text('Aeromoça 1'), Sg.Combo(aeromocas, key='aeromoca1')],
            [Sg.Text('Aeromoça 2'), Sg.Combo(aeromocas, key='aeromoca2')],
            [Sg.Button('Adicionar', size=(10, 1)), Sg.Button('Cancelar', size=(10, 1))]
        ]
        self.janela = Sg.Window('Adicionar Voo', layout)

    def validar_dados(self, valores):
        try:
            # Validação da Aeronave
            if not valores['aeronave']:
                raise ValueError("Entrada em 'aeronave' inválida, tente novamente")

            # Validação da Origem
            if len(valores['origem']) < 3:
                raise ValueError("Entrada em 'origem' inválida, tente novamente")

            # Validação do Destino
            if len(valores['destino']) < 3 or valores['destino'] == valores['origem']:
                raise ValueError("Entrada em 'destino' inválida, tente novamente")

            # Validação da Data
            data = datetime.strptime(valores['data'], '%d/%m/%Y')
            if data <= datetime.now():
                raise ValueError("Entrada em 'data' inválida, tente novamente")

            # Validação do Piloto
            if not valores['piloto']:
                raise ValueError("Entrada em 'piloto' inválida, tente novamente")

            # Validação do Copiloto
            if not valores['copiloto']:
                raise ValueError("Entrada em 'copiloto' inválida, tente novamente")

            # Validação da Aeromoça 1
            if not valores['aeromoca1']:
                raise ValueError("Entrada em 'aeromoça 1' inválida, tente novamente")

            # Validação da Aeromoça 2
            if not valores['aeromoca2']:
                raise ValueError("Entrada em 'aeromoça 2' inválida, tente novamente")

            # Validação da Hora de Decolagem
            hora = datetime.strptime(valores['hora'], '%H:%M').time()
            if hora.hour >= 24 or hora.minute >= 60:
                raise ValueError("Entrada em 'hora de decolagem' inválida, tente novamente")

            return True, "Dados válidos", data, hora

        except ValueError as e:
            Sg.popup(str(e))
            self.janela.close()
            return False, str(e), None, None

    def abrir(self):
        while True:
            evento, valores = self.janela.read()
            if evento == Sg.WINDOW_CLOSED or evento == 'Cancelar':
                break
            elif evento == 'Adicionar':
                # Validação dos dados
                sucesso, mensagem, data, hora = self.validar_dados(valores)
                if not sucesso:
                    break

                # Gerar código automaticamente (incrementando a quantidade de voos cadastrados)
                codigo_voo = self.controlador.controlador_voo.gerar_codigo_voo()

                # Cadastro de voo no sistema
                sucesso, mensagem = self.controlador.cadastrar_voo(
                    codigo_voo, valores['aeronave'], valores['origem'], valores['destino'],
                    valores['data'], valores['hora'], valores['piloto'], valores['copiloto'],
                    valores['aeromoca1'], valores['aeromoca2'],
                )


                # Exibir mensagem de confirmação ou erro
                if sucesso:
                    Sg.popup("Cadastro de voo realizado com sucesso")
                    break
                else:
                    Sg.popup(mensagem or "Falha no cadastro do voo, verifique os dados e tente novamente.")

        self.janela.close()
