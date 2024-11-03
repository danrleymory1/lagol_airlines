import PySimpleGUI as Sg
from PySimpleGUI import popup
from view import ViewAlterarVoo, ViewAdicionarVoo, ViewExcluirVoo  # Importa a nova ViewExcluirVoo

class ViewVerVoos:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        layout = [
            [Sg.Button('Adicionar Voo', size=(12, 1)), Sg.Button('Retornar', size=(10, 1))],
            [Sg.Text('Ver Voos', font=("Arial", 14))],
            [Sg.Column([[Sg.Text(f"{'Origem':<20} {'Destino':<20} {'Data':<15}")]])],
            [Sg.Column(self.carregar_voos(), scrollable=True, vertical_scroll_only=True, size=(500, 300))],
        ]
        self.janela = Sg.Window('Ver Voos', layout, size=(600, 500))

    def carregar_voos(self):
        voos = self.controlador.controlador_voo.buscar_todos_voos()
        voos_layout = []
        if voos:
            for voo in voos:
                voos_layout.append([
                    Sg.Text(f"{voo.origem:<20} {voo.destino:<20} {voo.data.strftime('%d/%m/%Y')}"),
                    Sg.Button('Alterar', key=f'alterar_{voo.cod}', size=(8, 1)),
                    Sg.Button('Deletar', key=f'deletar_{voo.cod}', size=(8, 1))
                ])
        else:
            voos_layout.append([Sg.Text("Nenhum voo cadastrado.")])
        return voos_layout

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED or evento == 'Retornar':
                self.janela.close()
                break
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
                self.janela.hide()
                view_excluir = ViewExcluirVoo(self.controlador, cod_voo)
                if view_excluir.abrir():  # Abre a view e verifica se o voo foi excluído
                    self.atualizar_voos()  # Atualiza a lista de voos se a exclusão foi bem-sucedida
                self.janela.un_hide()

    def atualizar_voos(self):
        # Recarrega a janela para exibir voos atualizados
        for element in self.janela.element_list():
            element.update(visible=False)
        self.janela.extend_layout(self.janela, [[Sg.Column(self.carregar_voos(), scrollable=True, vertical_scroll_only=True, size=(500, 300))]])
