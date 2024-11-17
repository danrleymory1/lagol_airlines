from dao.DAOVoo import DAOVoo
from model.Voos import Voos
from model.Aeronaves import Aeronaves
from model.Pessoas.Pilotos import Pilotos
from model.Pessoas.Aeromocas import Aeromocas
from datetime import datetime

class ControladorVoo:
    def __init__(self):
        self.dao_voos = DAOVoo()

    def gerar_codigo_voo(self):
        # Gera um código de voo automaticamente, incrementando a partir do último código.
        voos = self.dao_voos.buscar_voos()
        if voos:
            return max([voo.cod for voo in voos]) + 1  # Incrementa o código do voo
        else:
            return 1  # Caso não haja voos registrados, começa do código 1

    def cadastrar_voo(self, aeronave, origem, destino, data, hora, piloto, copiloto, aeromoca1, aeromoca2):
        
        # Validações
        if not isinstance(aeronave, Aeronaves):
            return False, "Aeronave inválida."
        
        if not isinstance(origem, str) or len(origem) < 3:
            return False, "Origem inválida."
        
        if not isinstance(destino, str) or len(destino) < 3 or destino == origem:
            return False, "Destino inválido."
        
        try:
            data = datetime.strptime(data, "%d/%m/%Y")
            if data <= datetime.now():
                return False, "Data inválida."
        except ValueError:
            return False, "Formato de data inválido."
        
        if not isinstance(piloto, Pilotos):
            return False, "Piloto inválido."
        
        if not isinstance(copiloto, Pilotos):
            return False, "Copiloto inválido."
        
        if not isinstance(aeromoca1, Aeromocas):
            return False, "Aeromoça 1 inválida."
        
        if not isinstance(aeromoca2, Aeromocas):
            return False, "Aeromoça 2 inválida."
        
        try:
            horario = datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            return False, "Formato de horário inválido."

        # Gerar código único
        codigo_voo = self.gerar_codigo_voo()

        # Criar o voo
        voo = Voos(
            cod=codigo_voo,
            aeronave=aeronave,
            assentos={},  # Implementar lógica para definir assentos
            origem=origem,
            destino=destino,
            data=data,
            horario_decolagem=hora,
            piloto=piloto,
            copiloto=copiloto,
            aeromoca1=aeromoca1,
            aeromoca2=aeromoca2
        )

        # Persistir voo
        if self.dao_voos.adicionar(voo):
            return True, "Voo cadastrado com sucesso!"
        else:
            return False, "Erro ao cadastrar o voo."


    def buscar_todos_voos(self):
        try:
            return self.dao_voos.buscar_voos()
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
        #RETIRAR ESSA BUSCA POR VOO
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
