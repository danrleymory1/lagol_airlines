import PySimpleGUI as Sg

class ViewExcluirVoo:
    def __init__(self, controlador, cod_voo):
        self.controlador = controlador
        self.cod_voo = cod_voo
        self.janela = None
        self.criar_janela()

    def criar_janela(self):
        layout = [
            [Sg.Text("Tem certeza que deseja excluir este voo?")],
            [Sg.Button("Confirmar", key="confirmar"), Sg.Button("Cancelar", key="cancelar")]
        ]
        self.janela = Sg.Window("Excluir Voo", layout)

    def abrir(self):
        while True:
            evento, valores = self.janela.read()

            if evento == Sg.WINDOW_CLOSED or evento == "cancelar":
                Sg.popup("Seu voo NÃO foi excluído!")  # Mensagem ao cancelar a exclusão
                self.janela.close()
                return False  # Retorna False se o usuário cancelou a operação
            elif evento == "confirmar":
                # Tenta deletar o voo e mostra a mensagem correspondente
                sucesso, mensagem = self.controlador.controlador_voo.deletar_voo(self.cod_voo)
                
                if sucesso:
                    Sg.popup("Voo excluído com sucesso!")  # Mensagem de exclusão bem-sucedida
                else:
                    Sg.popup("Erro: voo não encontrado.")  # Mensagem de erro se o voo não existir
                
                self.janela.close()
                return sucesso  # Retorna True se o voo foi deletado com sucesso
