import PySimpleGUI as Sg

class TelaAlterarCliente:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        layout = [
            [Sg.Push(), Sg.Text("Nome:"), Sg.InputText(key='nome'), Sg.Push()],
            [Sg.Push(), Sg.Text('Data de Nascimento:'), Sg.Input(key='data_nascimento'), Sg.CalendarButton('Data', target='data_nascimento', format='%d/%m/%Y'), Sg.Push()],
            [Sg.Push(), Sg.Text("Nova Senha (opcional):"), Sg.InputText(key='nova_senha', password_char='*'), Sg.Push()],
            [Sg.Push(), Sg.Text("Confirme a Nova Senha:"), Sg.InputText(key='confirma_nova_senha', password_char='*'), Sg.Push()],
            [Sg.Push(), Sg.Button("Salvar Alterações"), Sg.Button("Deletar Cliente"), Sg.Button("Cancelar"), Sg.Push()]
        ]

        # Cria a janela
        self.janela = Sg.Window("Alterar Cliente", layout, size=(400, 300))

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED or evento == 'Cancelar':
                self.retornar_cliente()
                break
            elif evento == 'Salvar Alterações':
                self.alterar_cliente(valores)
            elif evento == 'Deletar Cliente':
                self.deletar_cliente()

        self.janela.close()

    def alterar_cliente(self, valores):
        nome = valores['nome']
        data_nascimento = valores['data_nascimento']
        senha = valores['nova_senha']
        confirma_nova_senha = valores['confirma_nova_senha']

        sucesso, mensagem = self.controlador.controlador_cliente.alterar_dados_cliente(nome, data_nascimento, senha, confirma_nova_senha)

        if sucesso:
            Sg.popup("Sucesso", mensagem)
            self.janela.close()
            from view.ViewCliente import TelaCliente
            TelaCliente(self.controlador).abrir()
        else:
            Sg.popup("Erro", mensagem)

    def deletar_cliente(self):
        resposta = Sg.popup_yes_no("Tem certeza que deseja deletar este cliente?")
        if resposta == 'Yes':
            # Adicione a lógica de deletar cliente aqui
            sucesso, mensagem = self.controlador.controlador_cliente.deletar_cliente()
            if sucesso:
                Sg.popup("Sucesso", mensagem)
                self.janela.close()
                from view.ViewLogin import TelaLogin  # Supondo que você quer voltar para a tela de login
                TelaLogin(self.controlador).abrir()
            else:
                Sg.popup("Erro", mensagem)

    def retornar_cliente(self):
        self.janela.close()
        from view.ViewCliente import TelaCliente
        TelaCliente(self.controlador).abrir()
