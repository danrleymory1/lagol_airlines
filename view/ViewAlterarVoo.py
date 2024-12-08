import PySimpleGUI as Sg
from datetime import datetime

class ViewAlterarVoo:
    def __init__(self, controlador, voo):
        self.controlador = controlador
        self.voo = voo
        if not self.voo:
            raise ValueError("Não foi possível encontrar o voo para alterar.")
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        aeronaves = self.controlador.controlador_aeronave.listar_aeronaves()
        avioes = [aeronave.modelo.name for aeronave in aeronaves] if aeronaves else []

        todos_funcionarios = self.controlador.controlador_funcionario.buscar_todos_funcionarios()
        pilotos = [f"{funcionario.cpf} - {funcionario.nome}" for funcionario in todos_funcionarios if funcionario.cargo == "Piloto"]
        copilotos = pilotos
        aeromocas = [f"{funcionario.cpf} - {funcionario.nome}" for funcionario in todos_funcionarios if funcionario.cargo == "Aeromoca"]

        hora_decolagem = self.voo.horario_decolagem
        horas = f"{hora_decolagem.hour:02d}"
        minutos = f"{hora_decolagem.minute:02d}"

        layout = [

            [Sg.Text('Aeronave'), Sg.Combo(avioes, key='aeronave', default_value=self.voo.aeronave, disabled=True)],
            [Sg.Text('Origem'), Sg.Input(key='origem', default_text=self.voo.origem)],
            [Sg.Text('Destino'), Sg.Input(key='destino', default_text=self.voo.destino)],
            [Sg.Text('Data (dd/mm/yyyy)'), Sg.Input(key='data', default_text=self.voo.data.strftime('%d/%m/%Y'))],
            [Sg.Text('Hora de Decolagem'),
             Sg.Combo([f"{h:02d}" for h in range(24)], key='hora', readonly=True, size=(5, 1), default_value=horas),
             Sg.Text(':'),  # Espaço
             Sg.Combo([f"{m:02d}" for m in range(0, 60, 5)], key='minuto', readonly=True, size=(5, 1), default_value=minutos)]
            ,
            [Sg.Text('Piloto'), Sg.Combo(pilotos, key='piloto', default_value=self.voo.piloto)],
            [Sg.Text('Copiloto'), Sg.Combo(copilotos, key='copiloto', default_value=self.voo.copiloto)],
            [Sg.Text('Aeromoça 1'), Sg.Combo(aeromocas, key='aeromoca1', default_value=self.voo.aeromoca1)],
            [Sg.Text('Aeromoça 2'), Sg.Combo(aeromocas, key='aeromoca2', default_value=self.voo.aeromoca2)],
            [Sg.Button('Alterar', size=(10, 1)), Sg.Button('Cancelar', size=(10, 1))]
        ]
        self.janela = Sg.Window('Alterar Voo', layout)

    def abrir(self):
        while True:
            evento, valores = self.janela.read()
            if evento == Sg.WINDOW_CLOSED or evento == 'Cancelar':
                break
            elif evento == 'Alterar':
                # Construção da hora completa
                hora_selecionada = valores['hora']
                minuto_selecionado = valores['minuto']
                if not hora_selecionada or not minuto_selecionado:
                    Sg.popup("Hora de decolagem inválida. Selecione a hora e os minutos.")
                    continue
                hora_completa = f"{hora_selecionada}:{minuto_selecionado}"

                # Alteração do voo
                sucesso, mensagem = self.controlador.controlador_voo.alterar_voo(
                    self.voo,
                    valores['aeronave'], valores['origem'], valores['destino'],
                    valores['data'], hora_completa, valores['piloto'], valores['copiloto'],
                    valores['aeromoca1'], valores['aeromoca2']
                )
                Sg.popup(mensagem)
                if sucesso:
                    break

        self.janela.close()

