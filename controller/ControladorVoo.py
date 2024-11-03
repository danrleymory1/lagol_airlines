from dao.DAOVoos import DAOVoos
from model.Voos import Voos
from model.Aeronaves import Aeronaves
from model.Pessoas import Pilotos, Aeromocas

class ControladorVoo:
    def __init__(self):
        self.dao_voos = DAOVoos()

    def cadastrar_voos(self, origem, destino, aeromocas, pilotos, data, horario, aeronave, assentos):
        # Verificações detalhadas de parâmetros
        if not origem or not isinstance(origem, str):
            return False, "Erro: Origem inválida."
        if not destino or not isinstance(destino, str):
            return False, "Erro: Destino inválido."
        if not aeromocas or not isinstance(aeromocas, list):
            return False, "Erro: Aeromoças deve ser uma lista."
        if not pilotos or not isinstance(pilotos, list):
            return False, "Erro: Pilotos deve ser uma lista."
        if not data:
            return False, "Erro: Data inválida."
        if not horario:
            return False, "Erro: Horário inválido."
        if not aeronave or not isinstance(aeronave, Aeronaves):
            return False, "Erro: Aeronave inválida."
        if not assentos:
            return False, "Erro: Assentos inválidos."

        voo = Voos(origem=origem, destino=destino, aeromoca=aeromocas, piloto=pilotos, data=data, horario=horario, aeronave=aeronave, assentos=assentos)
        if self.dao_voos.adicionar(voo):
            return True, "Cadastro do voo realizado com sucesso!"
        else:
            return False, "Erro ao cadastrar o voo."

    def buscar_todos_voos(self):
        try:
            return self.dao_voos.buscar_todos()
        except Exception as e:
            print(f"Erro ao buscar todos os voos: {e}")
            return []

    def buscar_voo_por_codigo(self, cod):
        try:
            return self.dao_voos.buscar_por_codigo(cod)
        except Exception as e:
            print(f"Erro ao buscar voo: {e}")
            return None

    def alterar_voo(self, cod, nova_aeronave=None, novos_assentos=None, nova_origem=None, novo_destino=None, nova_data=None, novo_piloto=None, nova_aeromoca=None):
        voo = self.buscar_voo_por_codigo(cod)
        if not voo:
            return False, "Voo não encontrado."

        # Atualizar informações do voo com verificações de parâmetros
        try:
            if nova_aeronave:
                voo.aeronave = nova_aeronave
            if novos_assentos:
                voo.assentos = novos_assentos
            if nova_origem:
                voo.origem = nova_origem
            if novo_destino:
                voo.destino = novo_destino
            if nova_data:
                voo.data = nova_data
            if novo_piloto:
                voo.piloto = novo_piloto
            if nova_aeromoca:
                voo.aeromoca = nova_aeromoca

            if self.dao_voos.atualizar(voo):
                return True, "Dados do voo alterados com sucesso!"
        except Exception as e:
            print(f"Erro ao atualizar voo: {e}")
            return False, "Erro ao alterar os dados do voo."

    def deletar_voo(self, cod):
        voo = self.buscar_voo_por_codigo(cod)
        if not voo:
            return False, "Voo não encontrado."

        try:
            if self.dao_voos.deletar(cod):
                return True, "Voo deletado com sucesso!"
        except Exception as e:
            print(f"Erro ao deletar voo: {e}")
        return False, "Erro ao deletar o voo."
