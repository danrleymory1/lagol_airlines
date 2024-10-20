import PySimpleGUI as Sg
from PySimpleGUI import popup


class TelaFuncionarios:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        # Cabeçalho e layout inicial
        layout = [
            [Sg.Button('Retornar', size=(10, 1)), Sg.Push()],
            [Sg.Push(), Sg.Text('Gerenciar Funcionários', font=("Arial", 14)), Sg.Push()],
            [Sg.Column([[Sg.Text(f"{'CPF':<15} {'Nome':<20} {'Cargo':<15}")]])],  # Cabeçalho da lista
            [Sg.Column(self.carregar_funcionarios(), scrollable=True, vertical_scroll_only=True, size=(500, 300))],
            [Sg.Push(), Sg.Button('Adicionar Funcionário', size=(10, 2)), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window('Gerenciar Funcionários', layout, size=(600, 500))

    def carregar_funcionarios(self):
        funcionarios = self.controlador.controlador_funcionario.buscar_todos_funcionarios()
        if funcionarios:
            funcionarios_layout = []
            for funcionario in funcionarios:
                funcionarios_layout.append([
                    Sg.Text(f"{funcionario.cpf:<15} {funcionario.nome:<20} {funcionario.cargo:<15}"),
                    Sg.Push(),
                    Sg.Button('Alterar', key=f'alterar_{funcionario.cpf}', size=(10, 1)),
                    Sg.Button('Deletar', key=f'deletar_{funcionario.cpf}', size=(10, 1))  # Botão de deletar
                ])
            return funcionarios_layout
        else:
            Sg.popup("Informação", "Nenhum funcionário cadastrado.")
            return [[Sg.Text("Nenhum funcionário cadastrado.")]]

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED or evento == 'Retornar':
                self.retornar_tela_admin()
                break
            elif evento == 'Adicionar Funcionário':
                self.adicionar_funcionario()
            elif evento.startswith('alterar_'):
                funcionario_cpf = evento.split('_')[1]
                self.abrir_tela_alterar_funcionario(funcionario_cpf)
            elif evento.startswith('deletar_'):  # Verifica se o evento é de deletar
                funcionario_cpf = evento.split('_')[1]
                self.deletar_funcionario(funcionario_cpf)  # Chama a função de deletar

        self.janela.close()

    def adicionar_funcionario(self):
        self.janela.close()
        from view.ViewCadastroFuncionario import TelaCadastroFuncionario
        TelaCadastroFuncionario(self.controlador).abrir()

    def abrir_tela_alterar_funcionario(self, funcionario_cpf):
        funcionario = self.controlador.controlador_funcionario.buscar_funcionario_por_cpf(funcionario_cpf)
        if funcionario:
            self.janela.close()
            from view.ViewAlterarFuncionario import TelaAlterarFuncionario
            TelaAlterarFuncionario(self.controlador, funcionario).abrir()
        else:
            Sg.popup_error("Erro", "Funcionário não encontrado.")

    def deletar_funcionario(self, funcionario_cpf):
        resposta = Sg.popup_yes_no("Confirmar Deleção", f"Você tem certeza que deseja deletar o funcionário com CPF: {funcionario_cpf}?")
        if resposta == 'Yes':
            sucesso, mensagem = self.controlador.controlador_funcionario.deletar_funcionario(funcionario_cpf)
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
