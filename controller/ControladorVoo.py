from dao.DAOVoo import DAOVoo
from model.Voos import Voos
from dao.DAOAeronaves import DAOAeronaves
from model.Aeronaves import Aeronaves
from model.Pessoas.Pilotos import Pilotos
from model.Pessoas.Aeromocas import Aeromocas
from datetime import datetime

class ControladorVoo:
    def __init__(self, controlador):
        self.dao_voos = DAOVoo()
        self.__controlador = controlador
        self.dao_aeronave = DAOAeronaves()

    def gerar_codigo_voo(self):
        # Gera um código de voo automaticamente, incrementando a partir do último código.
        voos = self.dao_voos.buscar_voos()
        if voos:
            return max([voo.cod for voo in voos]) + 1  # Incrementa o código do voo
        else:
            return 1  # Caso não haja voos registrados, começa do código 1

    def cadastrar_voo(self, aeronave, origem, destino, data, hora, piloto, copiloto, aeromoca1, aeromoca2):
        try:
            if not aeronave or len(origem) < 3 or len(destino) < 3 or origem == destino or not data or not hora:
                raise ValueError("Dados inválidos para cadastro do voo.")
            if not piloto or not copiloto or piloto == copiloto or not aeromoca1 or not aeromoca2 or aeromoca1 == aeromoca2:
                raise ValueError("Tripulação inválida.")

            data_obj = datetime.strptime(data, '%d/%m/%Y')
            hora_obj = datetime.strptime(hora, '%H:%M').time()
            if data_obj <= datetime.now():
                raise ValueError("Data inválida.")

            codigo_voo = self.gerar_codigo_voo()
            aeronave_obj = self.dao_aeronave.buscar_por_modelo(aeronave)
            if not aeronave_obj:
                raise ValueError("Aeronave não encontrada.")
            
            assentos = []
            for fileira in range(1, aeronave_obj.fileiras + 1):
                for coluna in range(aeronave_obj.assentos_por_fileira):
                    assento = f"{fileira}{chr(65 + coluna)}"
                    assentos.append({assento: None})
            
            voo = Voos(cod=codigo_voo, aeronave=aeronave_obj, assentos=assentos, origem=origem, destino=destino,
                       data=data_obj, horario_decolagem=hora_obj, piloto=piloto, copiloto=copiloto, aeromoca1=aeromoca1,
                       aeromoca2=aeromoca2)

            if self.dao_voos.adicionar(voo):
                return True, "Voo cadastrado com sucesso."
            return False, "Erro ao cadastrar voo."
        except ValueError as e:
            return False, str(e)

    def buscar_todos_voos(self):
        try:
            return self.dao_voos.buscar_voos()
        except Exception as e:
            print(f"Erro ao buscar todos os voos: {e}")
            return []

    def buscar_voo_por_codigo(self, cod):
        try:
            voo_dict = self.dao_voos.buscar_por_codigo(cod)
            if voo_dict:
                return self.dao_voos.dict_to_voo(voo_dict)
            return None
        except Exception as e:
            print(f"Erro ao buscar voo: {e}")
            return None

    def alterar_voo(self, voo, aeronave=None, origem=None, destino=None, data=None, hora=None, piloto=None,
                    copiloto=None, aeromoca1=None, aeromoca2=None):
        try:
            # Validações de entrada
            if origem and len(origem) < 3:
                raise ValueError("Origem inválida.")
            if destino and (len(destino) < 3 or destino == origem):
                raise ValueError("Destino inválido.")
            if piloto and copiloto and piloto == copiloto:
                raise ValueError("Piloto e copiloto não podem ser a mesma pessoa.")
            if aeromoca1 and aeromoca2 and aeromoca1 == aeromoca2:
                raise ValueError("As aeromoças não podem ser a mesma pessoa.")
            if data:
                data_obj = datetime.strptime(data, '%d/%m/%Y')
                if data_obj <= datetime.now():
                    raise ValueError("Data inválida.")
            if hora:
                hora_obj = datetime.strptime(hora, '%H:%M').time()
            else:
                hora_obj = voo.horario_decolagem

            # Busca a aeronave se necessário
            if aeronave:
                aeronave_obj = self.dao_aeronave.buscar_por_modelo(aeronave)
                if not aeronave_obj:
                    raise ValueError("Aeronave não encontrada.")
                voo.aeronave = aeronave_obj  # Atualiza com o objeto aeronave correto

            # Atualiza os campos do voo
            if origem:
                voo.origem = origem
            if destino:
                voo.destino = destino
            if data:
                voo.data = data_obj
            if hora:
                voo.horario_decolagem = hora_obj
            if piloto:
                voo.piloto = piloto
            if copiloto:
                voo.copiloto = copiloto
            if aeromoca1:
                voo.aeromoca1 = aeromoca1
            if aeromoca2:
                voo.aeromoca2 = aeromoca2

            # Persistir no DAO
            sucesso = self.dao_voos.atualizar(voo)
            if sucesso:
                return True, "Voo alterado com sucesso."
            else:
                return False, "Erro ao alterar voo."
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            print(f"Erro inesperado ao alterar voo: {e}")
            return False, "Erro inesperado ao alterar voo."

    def deletar_voo(self, cod):
        voo = self.buscar_voo_por_codigo(cod)
        if not voo:
            return False, "Voo não encontrado."

        try:
            if self.dao_voos.deletar(cod):
                self.__controlador.controlador_reserva.deletar_reservas_por_voo(cod)
                return True, "Voo deletado com sucesso!"
        except Exception as e:
            print(f"Erro ao deletar voo: {e}")
        return False, "Erro ao deletar o voo."
