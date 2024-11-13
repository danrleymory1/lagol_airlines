import sys
import PySimpleGUI as Sg
from PySimpleGUI import popup
from view.ViewAdicionarVoo import ViewAdicionarVoo
from view.ViewAlterarVoo import ViewAlterarVoo


class TelaVerVoosAdm:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        layout = [
            [Sg.Button('Adicionar Voo', size=(12, 1)), Sg.Button('Retornar', size=(10, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text('Ver Voos', font=("Arial", 14)), Sg.Push()],
            [Sg.Column([[Sg.Text(f"{'Origem':<20} {'Destino':<20} {'Data':<15} {'Horario'}")]])],  # Cabeçalho da lista
            [Sg.Column(self.carregar_voos(), scrollable=True, vertical_scroll_only=True, size=(500, 300))],
        ]
        self.janela = Sg.Window('Ver Voos', layout, size=(600, 500))

    def carregar_voos(self):
        voos = self.controlador.controlador_voo.buscar_todos_voos()
        voos_layout = []
        if voos:
            for voo in voos:
                voos_layout.append([
                    Sg.Text(f"{voo.origem:<20} {voo.destino:<20} {voo.data.strftime('%d/%m/%Y')} {voo.horario_decolagem:<8}"),
                    Sg.Push(),
                    Sg.Button('Alterar', key=f'alterar_{voo.cod}', size=(8, 1)),
                    Sg.Button('Deletar', key=f'deletar_{voo.cod}', size=(8, 1))
                ])
        else:
            voos_layout.append([Sg.Text("Nenhum voo cadastrado.")])
        return voos_layout

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED:
                sys.exit()
            elif evento == 'Retornar':
                self.retornar_tela_adm()
            elif evento == 'Adicionar Voo':
                self.janela.hide()
                ViewAdicionarVoo(self.controlador).abrir()
                self.janela.un_hide()
                self.atualizar_voos()
            elif evento.startswith('alterar_'):
                cod_voo = evento.split('_')[1]
                voo = self.controlador.controlador_voo.buscar_voo_por_codigo(cod_voo)
                if voo:
                    self.janela.hide()
                    ViewAlterarVoo(self.controlador, voo).abrir()
                    self.janela.un_hide()
                    self.atualizar_voos()
            elif evento.startswith('deletar_'):
                cod_voo = evento.split('_')[1]
                res = Sg.popup("Tem certeza que deseja excluir este voo?", title="Excluir Voo",  custom_text=("Confirmar", "Cancelar"))
                if res == "Confirmar":
                    try:
                        self.controlador.controlador_voo.deletar_voo(cod_voo)
                    except Exception as e:
                        popup(f"Erro ao excluir voo: {e}")
                    Sg.popup("Voo excluído com sucesso.")
                    self.atualizar_voos()
                else:
                    Sg.popup("Seu voo NÃO foi excluído!")

    def atualizar_voos(self):
        self.janela.close()
        self.criar_janela()
        self.carregar_voos()

    def retornar_tela_adm(self):
        self.janela.close()
        from view.ViewAdmin import TelaAdmin
        TelaAdmin(self.controlador).abrir()
