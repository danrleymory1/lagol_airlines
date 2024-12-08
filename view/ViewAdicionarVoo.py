import PySimpleGUI as Sg
from datetime import datetime

class ViewAdicionarVoo:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        aeronaves = self.controlador.controlador_aeronave.listar_aeronaves()
        avioes = [aeronave.modelo.name for aeronave in aeronaves] if aeronaves else []

        todos_funcionarios = self.controlador.controlador_funcionario.buscar_todos_funcionarios()
        pilotos = [f"{funcionario.cpf} - {funcionario.nome}" for funcionario in todos_funcionarios if funcionario.cargo == "Piloto"]
        copilotos = pilotos  # Mesmo filtro de pilotos
        aeromocas = [f"{funcionario.cpf} - {funcionario.nome}" for funcionario in todos_funcionarios if funcionario.cargo == "Aeromoca"]

        layout = [
            [Sg.Text('Aeronave'), Sg.Combo(avioes, key='aeronave', readonly=True)],
            [Sg.Text('Origem'), Sg.Input(key='origem')],
            [Sg.Text('Destino'), Sg.Input(key='destino')],
            [Sg.Text('Data (dd/mm/yyyy)'), Sg.Input(key='data', readonly=True), Sg.CalendarButton('Selecionar Data', target='data', format='%d/%m/%Y')],
            [Sg.Text('Hora de Decolagem'),
             Sg.Combo([f"{h:02d}" for h in range(24)], key='hora', readonly=True, size=(5, 1)),
             Sg.Text(':'),  # Espaço
             Sg.Combo([f"{m:02d}" for m in range(0, 60, 5)], key='minuto', readonly=True, size=(5, 1))]
            ,
            [Sg.Text('Piloto'), Sg.Combo(pilotos, key='piloto', readonly=True)],
            [Sg.Text('Copiloto'), Sg.Combo(copilotos, key='copiloto', readonly=True)],
            [Sg.Text('Aeromoça 1'), Sg.Combo(aeromocas, key='aeromoca1', readonly=True)],
            [Sg.Text('Aeromoça 2'), Sg.Combo(aeromocas, key='aeromoca2', readonly=True)],
            [Sg.Button('Adicionar', size=(10, 1)), Sg.Button('Cancelar', size=(10, 1))]
        ]
        self.janela = Sg.Window('Adicionar Voo', layout)

    def abrir(self):
        while True:
            evento, valores = self.janela.read()
            if evento == Sg.WINDOW_CLOSED or evento == 'Cancelar':
                break
            elif evento == 'Adicionar':
                # Construção da hora completa
                hora_selecionada = valores['hora']
                minuto_selecionado = valores['minuto']
                if not hora_selecionada or not minuto_selecionado:
                    Sg.popup("Entrada em 'Hora de decolagem' inválida, tente novamente")
                    continue
                hora_completa = f"{hora_selecionada}:{minuto_selecionado}"

                # Cadastro do voo
                sucesso, mensagem = self.controlador.controlador_voo.cadastrar_voo(
                    valores['aeronave'], valores['origem'], valores['destino'],
                    valores['data'], hora_completa, valores['piloto'], valores['copiloto'],
                    valores['aeromoca1'], valores['aeromoca2']
                )
                Sg.popup(mensagem)
                if sucesso:
                    break

        self.janela.close()
