from model.Reservas import Reservas
from dao.DAOReserva import DAOReserva
from dao.DAOVoo import DAOVoo
from dao.DAOAeronaves import DAOAeronaves
import random
import string

class ControladorReserva:
    def __init__(self):
        self.__dao_reserva = DAOReserva()
        self.__dao_voo = DAOVoo()
        self.__dao_aeronave = DAOAeronaves()

    def cadastrar_reserva(self, passageiro, cliente, voo_cod):
        while True:
            cod = ''.join(random.choices(string.digits + string.ascii_uppercase, k=5))
            if self.validar_codigo(cod):
                break

        voo = self.__dao_voo.buscar_por_codigo(voo_cod)
        if not voo:
            return False, "Voo não encontrado."

        reserva = Reservas(cod=cod, passageiro=passageiro, cliente=cliente, voo=voo_cod, assento=None)

        if self.__dao_reserva.adicionar(reserva):
            return cod, "Reserva realizada com sucesso!"
        else:
            return False, "Erro ao cadastrar a reserva. Tente novamente."

    def validar_codigo(self, cod):
        if self.__dao_reserva.buscar_por_cod(cod):
            return False
        return True

    def buscar_reserva_por_cod(self, cod):
        return self.__dao_reserva.buscar_por_cod(cod)

    def buscar_reservas_por_cliente(self, cpf_cliente):
        return self.__dao_reserva.buscar_reservas({"cliente": cpf_cliente})

    def deletar_reserva(self, cod):
        reserva = self.__dao_reserva.buscar_por_cod(cod)
        if not reserva:
            return False, "Reserva não encontrada."

        sucesso = self.__dao_reserva.deletar(cod)
        if sucesso:
            self.liberar_assento(cod, reserva.assento)
            return True, "Reserva deletada com sucesso!"
        else:
            return False, "Erro ao deletar reserva. Tente novamente."

    def selecionar_assento_disponivel(self, aeronave, voo):
        total_assentos = [f"{row}{chr(65 + col)}" for row in range(1, aeronave.fileiras + 1) for col in range(aeronave.assentos_por_fileira)]
        ocupados = list(voo.assentos.values()) if isinstance(voo.assentos, dict) else []
        disponiveis = [assento for assento in total_assentos if assento not in ocupados]
        return disponiveis[0] if disponiveis else None

    def listar_fileiras_disponiveis(self, voo):
        aeronave = self.__dao_aeronave.buscar_por_modelo(voo.aeronave)
        if not aeronave:
            return []
        return [str(row) for row in range(1, aeronave.fileiras + 1)]

    def listar_assentos_disponiveis(self, voo_cod, fileira):
        voo = self.__dao_voo.buscar_por_codigo(voo_cod)
        if not voo:
            return []

        aeronave = self.__dao_aeronave.buscar_por_modelo(voo.aeronave)
        if not aeronave:
            return []

        total_assentos = [f"{fileira}{chr(65 + col)}" for col in range(aeronave.assentos_por_fileira)]
        ocupados = list(voo.assentos.values()) if isinstance(voo.assentos, dict) else []
        return [assento for assento in total_assentos if assento not in ocupados]
    
    def liberar_assento(self, reserva_cod, assento):

        reserva = self.__dao_reserva.buscar_por_cod(reserva_cod)
        if not reserva:
            return False, "Reserva não encontrada."

        voo = self.__dao_voo.buscar_por_codigo(reserva.voo)
        if not voo:
            return False, "Voo não encontrado."

        if assento not in voo.assentos:
            return False, "Assento não ocupado."
        else:
            del voo.assentos[assento]
            sucesso = self.__dao_voo.atualizar(voo)
            if sucesso:
                reserva.assento = None
                self.__dao_reserva.atualizar(reserva)
                return True, "Assento liberado com sucesso."
            else:
                return False, "Erro ao liberar o assento."

    def atualizar_assento(self, reserva_cod, novo_assento):
        reserva = self.__dao_reserva.buscar_por_cod(reserva_cod)
        if not reserva:
            return False, "Reserva não encontrada."

        voo = self.__dao_voo.buscar_por_codigo(reserva.voo)
        if not voo:
            return False, "Voo não encontrado."

        if novo_assento in list(voo.assentos.values()):
            return False, "Assento já ocupado."

        aeronave = self.__dao_aeronave.buscar_por_modelo(voo.aeronave)
        if not aeronave:
            return False, "Aeronave não encontrada."

        total_assentos = [f"{row}{chr(65 + col)}" for row in range(1, aeronave.fileiras + 1) for col in range(aeronave.assentos_por_fileira)]
        if novo_assento not in total_assentos:
            return False, "Assento inválido para esta aeronave."

        voo.assentos[novo_assento] = reserva.passageiro
        sucesso = self.__dao_voo.atualizar_assentos(voo.cod, reserva.cod, voo.assentos)
        if sucesso:
            reserva.assento = novo_assento
            self.__dao_reserva.atualizar_assento(reserva.cod, voo.assentos)
            return True, "Assento atualizado com sucesso."
        else:
            return False, "Erro ao atualizar o assento."

