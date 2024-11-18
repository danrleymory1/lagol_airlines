import PySimpleGUI as Sg
from datetime import datetime

class ViewAlterarVoo:
    def __init__(self, controlador, voo):
        self.controlador = controlador
        self.voo = voo  # Informações do voo a ser alterado
        if not self.voo:  # Verifica se self.voo é None
            raise ValueError("Não foi possível encontrar o voo para alterar.")
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Verificar se self.voo é None
        if not self.voo:
            Sg.popup("Erro: voo não encontrado!")
            return

        # Lista de opções para aviões, pilotos, copilotos e aeromoças
        avioes = ["Avião 1", "Avião 2", "Avião 3"]
        pilotos = ["Piloto 1", "Piloto 2"]
        copilotos = ["Copiloto 1", "Copiloto 2"]
        aeromocas = ["Aeromoça 1", "Aeromoça 2", "Aeromoça 3"]

        # Layout com os campos preenchidos com as informações do voo selecionado
        layout = [
            [Sg.Text('Aeronave'), Sg.Combo(avioes, default_value=self.voo.aeronave, key='aeronave')],
            [Sg.Text('Origem'), Sg.Input(default_text=self.voo.origem, key='origem')],
            [Sg.Text('Destino'), Sg.Input(default_text=self.voo.destino, key='destino')],
            [Sg.Text('Data (dd/mm/yyyy)'), Sg.Input(default_text=self.voo.data.strftime('%d/%m/%Y'), key='data')],
            [Sg.Text('Hora de Decolagem (hh:mm)'), Sg.Input(default_text=self.voo.hora.strftime('%H:%M'), key='hora')],
            [Sg.Text('Piloto'), Sg.Combo(pilotos, default_value=self.voo.piloto, key='piloto')],
            [Sg.Text('Copiloto'), Sg.Combo(copilotos, default_value=self.voo.copiloto, key='copiloto')],
            [Sg.Text('Aeromoça 1'), Sg.Combo(aeromocas, default_value=self.voo.aeromoca1, key='aeromoca1')],
            [Sg.Text('Aeromoça 2'), Sg.Combo(aeromocas, default_value=self.voo.aeromoca2, key='aeromoca2')],
            [Sg.Button('Salvar', size=(10, 1)), Sg.Button('Cancelar', size=(10, 1))]
        ]
        self.janela = Sg.Window('Alterar Voo', layout)

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
            elif evento == 'Salvar':
                # Validação dos dados
                sucesso, mensagem, data, hora = self.validar_dados(valores)
                if not sucesso:
                    break

                # Realizar a alteração do voo
                sucesso, mensagem = self.controlador.controlador_voo.alterar_voo(
                    self.voo.cod, valores['aeronave'], valores['origem'], valores['destino'],
                    data, hora, valores['piloto'], valores['copiloto'],
                    valores['aeromoca1'], valores['aeromoca2']
                )

                # Exibir a mensagem de confirmação ou erro
                if sucesso:
                    Sg.popup("Informação do voo alterado com sucesso!")
                    break
                else:
                    Sg.popup("Informação alterada inválida, por favor, tente novamente")

        self.janela.close()
