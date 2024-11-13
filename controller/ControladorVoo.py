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
            return max([voo.codigo for voo in voos]) + 1  # Incrementa o código do voo
        else:
            return 1  # Caso não haja voos registrados, começa do código 1

    def cadastrar_voo(self, aviao, origem, destino, data, horario, piloto, copiloto, aeromoca1, aeromoca2):
        # Verificação do Avião
        if not aviao or not isinstance(aviao, Aeronaves):
            return False, "Entrada em 'avião' inválida, tente novamente."

        # Verificação de Origem
        if not origem or not isinstance(origem, str) or len(origem) < 3:
            return False, "Entrada em 'origem' inválida, tente novamente."

        # Verificação de Destino
        if not destino or not isinstance(destino, str) or len(destino) < 3 or destino == origem:
            return False, "Entrada em 'destino' inválida, tente novamente."

        # Verificação de Data (deve ser futura e no formato dd/mm/aaaa)
        try:
            data = datetime.strptime(data, "%d/%m/%Y")
            if data <= datetime.now():
                return False, "Entrada em 'data' inválida, tente novamente."
        except ValueError:
            return False, "Entrada em 'data' inválida, tente novamente."

        # Verificação do Piloto
        if not piloto or not isinstance(piloto, Pilotos):
            return False, "Entrada em 'piloto' inválida, tente novamente."

        # Verificação do Copiloto
        if not copiloto or not isinstance(copiloto, Pilotos):
            return False, "Entrada em 'copiloto' inválida, tente novamente."

        # Verificação da Aeromoça 1
        if not aeromoca1 or not isinstance(aeromoca1, Aeromocas):
            return False, "Entrada em 'aeromoça 1' inválida, tente novamente."

        # Verificação da Aeromoça 2
        if not aeromoca2 or not isinstance(aeromoca2, Aeromocas):
            return False, "Entrada em 'aeromoça 2' inválida, tente novamente."

        # Verificação de Horário (deve estar no formato hh:mm e ser um horário válido)
        try:
            horario = datetime.strptime(horario, "%H:%M").time()
            if horario.hour < 0 or horario.hour >= 24:
                return False, "Entrada em 'hora de decolagem' inválida, tente novamente."
        except ValueError:
            return False, "Entrada em 'hora de decolagem' inválida, tente novamente."

        # Gerar o código automaticamente
        codigo_voo = self.gerar_codigo_voo()

        # Gerar o número de assentos com base no avião selecionado
        numero_assentos = aviao.obter_numero_assentos()

        # Se todas as verificações passarem, cria-se o voo
        voo = Voos(
            codigo=codigo_voo,  # Código gerado automaticamente
            origem=origem,
            destino=destino,
            aeromoca=[aeromoca1, aeromoca2],
            piloto=[piloto, copiloto],
            data=data,
            horario=horario,
            aeronave=aviao,
            assentos=numero_assentos  # Número de assentos gerado automaticamente
        )
        
        if self.dao_voos.adicionar(voo):
            return True, "Cadastro do voo realizado com sucesso!"
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
