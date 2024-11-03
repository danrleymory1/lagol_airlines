from dao.DAOVoos import DAOVoos
from model.Voos import Voos
from model.Aeronaves import Aeronaves
from model.Pessoas import Pilotos, Aeromocas
import datetime

class ControladorVoo:
    def __init__(self):
        self.dao_voos = DAOVoos()

    def buscar_todos_voos(self):
        try:
            return self.dao_voos.buscar_todos()
        except Exception as e:
            print(f"Erro ao buscar todos os voos: {e}")
            return []

    def adicionar_voo(self, cod, aeronave, assentos, origem, destino, data, piloto, aeromoca):
        try:
            voo = Voos(
                cod=cod,
                aeronave=aeronave,
                assentos=assentos,
                origem=origem,
                destino=destino,
                data=data,
                piloto=piloto,
                aeromoca=aeromoca
            )
            return self.dao_voos.adicionar(voo)
        except Exception as e:
            print(f"Erro ao adicionar voo: {e}")
            return False

    def buscar_voo_por_codigo(self, cod):
        try:
            return self.dao_voos.buscar_por_codigo(cod)
        except Exception as e:
            print(f"Erro ao buscar voo: {e}")
            return None

    def atualizar_voo(self, cod, nova_aeronave=None, novos_assentos=None, nova_origem=None, novo_destino=None, nova_data=None, novo_piloto=None, nova_aeromoca=None):
        voo = self.buscar_voo_por_codigo(cod)
        if not voo:
            print("Voo não encontrado.")
            return False

        # Atualizar informações do voo
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

            return self.dao_voos.atualizar(voo)
        except Exception as e:
            print(f"Erro ao atualizar voo: {e}")
            return False

    def deletar_voo(self, cod):
        try:
            return self.dao_voos.deletar(cod)
        except Exception as e:
            print(f"Erro ao deletar voo: {e}")
            return False
