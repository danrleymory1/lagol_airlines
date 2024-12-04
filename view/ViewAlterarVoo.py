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
        # Busca as aeronaves cadastradas no sistema
        aeronaves = self.controlador.controlador_aeronave.listar_aeronaves()
        avioes = [aeronave.modelo.name for aeronave in aeronaves] if aeronaves else []

        # Busca os pilotos e copilotos cadastrados no sistema
        todos_funcionarios = self.controlador.controlador_funcionario.buscar_todos_funcionarios()
        pilotos = [f"{funcionario.cpf} - {funcionario.nome}" for funcionario in todos_funcionarios if funcionario.cargo == "Piloto"]
        copilotos = [f"{funcionario.cpf} - {funcionario.nome}" for funcionario in todos_funcionarios if funcionario.cargo == "Piloto"]

        # Busca as aeromoças cadastradas no sistema
        aeromocas = [f"{funcionario.cpf} - {funcionario.nome}" for funcionario in todos_funcionarios if funcionario.cargo == "Aeromoca"]

        layout = [
            [Sg.Text('Aeronave'), Sg.Combo(avioes, key='aeronave',default_value=self.voo.aeronave)],
            [Sg.Text('Origem'), Sg.Input(key='origem', default_text=self.voo.origem)],
            [Sg.Text('Destino'), Sg.Input(key='destino', default_text=self.voo.destino)],
            [Sg.Text('Data (dd/mm/yyyy)'), Sg.Input(key='data', default_text=str(self.voo.data.day) + "/" + str(self.voo.data.month) + "/" + str(self.voo.data.year)), Sg.CalendarButton('Selecionar Data', target='data', format='%d/%m/%Y', default_date_m_d_y=(self.voo.data.month, self.voo.data.day, self.voo.data.year))],
            [Sg.Text('Hora de Decolagem'), Sg.Combo([f"{h:02d}:00" for h in range(24)], key='hora', default_value=self.voo.horario_decolagem)],
            [Sg.Text('Piloto'), Sg.Combo(pilotos, key='piloto', default_value=self.voo.piloto)],
            [Sg.Text('Copiloto'), Sg.Combo(copilotos, key='copiloto', default_value=self.voo.copiloto)],
            [Sg.Text('Aeromoça 1'), Sg.Combo(aeromocas, key='aeromoca1', default_value=self.voo.aeromoca1)],
            [Sg.Text('Aeromoça 2'), Sg.Combo(aeromocas, key='aeromoca2', default_value=self.voo.aeromoca2)],
            [Sg.Button('Alterar', size=(10, 1)), Sg.Button('Cancelar', size=(10, 1))]
        ]
        self.janela = Sg.Window('Alterar Voo', layout)

    def validar_dados(self, valores):
        try:
            # Validação da Aeronave
            if not valores['aeronave']:
                raise ValueError("Entrada em 'Avião' inválida, tente novamente")

            # Validação da Origem
            if len(valores['origem']) < 3:
                raise ValueError("Entrada em 'origem' inválida, tente novamente")

            # Validação do Destino
            if len(valores['destino']) < 3 or valores['destino'] == valores['origem']:
                raise ValueError("Entrada em 'destino' inválida, tente novamente")

            # Validação da Data
            if not valores['data']:  # Verifica se o campo de data está vazio
                raise ValueError("Entrada em 'data' inválida, tente novamente")
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
            return True, "Entrada em 'hora de decolagem' inválida, tente novamente", data, hora

        except ValueError as e:
            Sg.popup(str(e))
            return False, str(e), None, None

    def abrir(self):
        while True:
            evento, valores = self.janela.read()
            if evento == Sg.WINDOW_CLOSED or evento == 'Cancelar':
                break
            elif evento == 'Alterar':
                # Validação dos dados
                sucesso, mensagem, data, hora = self.validar_dados(valores)
                if not sucesso:
                    continue

                # Cadastro de voo no sistema

                print(f"Cod: {self.voo.cod}, data: {valores['data']}, Origem: {valores['origem']}, Destino: {valores['destino']}")

                print(self.voo)
                

                sucesso, mensagem = self.controlador.controlador_voo.alterar_voo(
                    self.voo,  # Passa o objeto voo diretamente
                    valores['aeronave'], valores['origem'], valores['destino'],
                    valores['data'], valores['hora'], valores['piloto'], valores['copiloto'],
                    valores['aeromoca1'], valores['aeromoca2']
                )


                if sucesso is None:
                    Sg.popup("Erro inesperado ao tentar alterar o voo.")
                    continue

                if sucesso:
                    Sg.popup("Informação do voo alterado com sucesso!")
                    break
                else:
                    Sg.popup("Informação alterada inválida, por favor, tente novamente")

        self.janela.close()
