import sys
import PySimpleGUI as Sg
from PySimpleGUI import popup
from model.ModeloAeronaves import ModeloAeronave

class TelaGerenciarAeronaves:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Cabeçalho e layout inicial
        layout = [
            [Sg.Button('Retornar', size=(10, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text('Gerenciar Aeronaves', font=("Arial", 14)), Sg.Push()],
            [Sg.Column([[Sg.Text(f"{'Modelo':<20} {'Fileiras':<10} {'Assentos':<10} {'Bagagens':<10}")]])],  # Cabeçalho da lista
            [Sg.Column(self.carregar_aeronaves(), scrollable=True, vertical_scroll_only=True, size=(500, 300))],
            [Sg.Push(), Sg.Button('Adicionar Aeronave', size=(15, 2)), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window('Gerenciar Aeronaves', layout, size=(600, 500))

    def carregar_aeronaves(self):
        aeronaves = self.controlador.controlador_aeronave.listar_aeronaves()
        if aeronaves:
            aeronaves_layout = []
            for aeronave in aeronaves:
                aeronaves_layout.append([
                    Sg.Text(f"{aeronave.modelo.name:<20} {aeronave.fileiras:<10} {aeronave.assentos_por_fileira:<10} {aeronave.max_bagagens:<10}"),
                    Sg.Push(),
                    Sg.Button('Deletar', key=f'deletar_{aeronave.modelo.name}', size=(10, 1))  # Botão de deletar
                ])
            return aeronaves_layout
        else:
            Sg.popup("Informação", "Nenhuma aeronave cadastrada.")
            return [[Sg.Text("Nenhuma aeronave cadastrada.")]]

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == 'Retornar':
                self.retornar_tela_admin()
                break
            elif evento == Sg.WINDOW_CLOSED:
                sys.exit()
            elif evento == 'Adicionar Aeronave':
                self.adicionar_aeronave()
            elif evento.startswith('deletar_'):
                modelo_nome = evento.split('_')[1]
                self.deletar_aeronave(modelo_nome)

        self.janela.close()

    def adicionar_aeronave(self):
        self.janela.close()
        TelaCadastroAeronave(self.controlador).abrir()

    def deletar_aeronave(self, modelo_nome):
        resposta = Sg.popup_yes_no("Confirmar Deleção", f"Você tem certeza que deseja deletar a aeronave modelo: {modelo_nome}?")
        if resposta == 'Yes':
            sucesso, mensagem = self.controlador.controlador_aeronave.deletar_aeronave(modelo_nome)
            if sucesso:
                Sg.popup("Sucesso", mensagem)
                self.janela.close()
                self.criar_janela()  # Recria a janela para atualizar a lista
            else:
                Sg.popup_error("Erro", mensagem)

    def retornar_tela_admin(self):
        self.janela.close()
        from view.ViewAdmin import TelaAdmin
        TelaAdmin(self.controlador).abrir()


class TelaCadastroAeronave:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        modelos = [modelo.name for modelo in ModeloAeronave]  # Lista de modelos do enum
        layout = [
            [Sg.Push(), Sg.Text("Cadastrar Aeronave", font=("Arial", 14)), Sg.Push()],
            [Sg.Push(), Sg.Text("Modelo:"), Sg.Combo(modelos, key='modelo', size=(30, 1)), Sg.Push()],
            [Sg.Push(), Sg.Button('Cadastrar', size=(10, 1)), Sg.Button('Cancelar', size=(10, 1)), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window('Cadastrar Aeronave', layout, size=(400, 200))

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == 'Cancelar':
                self.retornar_tela_aeronaves()
                break
            elif evento == Sg.WINDOW_CLOSED:
                sys.exit()
            elif evento == 'Cadastrar':
                self.cadastrar_aeronave(valores)

        self.janela.close()

    def cadastrar_aeronave(self, valores):
        modelo_nome = valores['modelo']

        if not modelo_nome:
            Sg.popup_error("Erro", "Selecione um modelo para cadastrar a aeronave.")
            return

        sucesso, mensagem = self.controlador.controlador_aeronave.cadastrar_aeronave(modelo_nome)

        if sucesso:
            Sg.popup("Sucesso", mensagem)
            self.janela.close()
            TelaGerenciarAeronaves(self.controlador).abrir()
        else:
            Sg.popup_error("Erro", mensagem)

    def retornar_tela_aeronaves(self):
        self.janela.close()
        TelaGerenciarAeronaves(self.controlador).abrir()
