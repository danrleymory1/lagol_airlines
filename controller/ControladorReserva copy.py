from model.Reservas import Reservas
from dao.DAOReserva import DAOReserva
import random
import string


class ControladorReserva:
    def __init__(self):
        self.__dao = DAOReserva()

    def cadastrar_reserva(self, passageiro, cliente, voo_cod):

        while True:
            cod = ''.join(random.choices(string.digits + string.ascii_uppercase, k=5))  # Junta os caracteres em uma string
            if self.validar_codigo(cod):
                break
        
        assento = str(random.randint(1, 30)) + random.choice("ABCDEF") #todo: verificar se o assento já está ocupado

        reserva = Reservas(cod=cod, passageiro=passageiro, cliente=cliente, voo=voo_cod, assento=assento)

        if self.__dao.adicionar(reserva):
            return cod, "Reserva realizada com sucesso!"
        else:
            return False, "Erro ao cadastrar a reserva. Tente novamente."
        
    def validar_codigo(self, cod):
        if self.__dao.buscar_por_cod(cod):
            return False
        return True

    def buscar_reserva_por_cod(self, cod):
        return self.__dao.buscar_por_cod(cod)
    
    def buscar_reservas_por_cliente(self, cpf_cliente):
        return self.__dao.buscar_reservas({"cliente": cpf_cliente})

    def deletar_reserva(self, cod):
        sucesso = self.__dao.deletar(cod)
        if sucesso:
            return True, "Reserva deletada com sucesso!"
        else:
            return False, "Erro ao deletar reserva. Tente novamente."

    def selecionar_assento_disponivel(self, voo):
        aeronave = voo.aeronave
        total_assentos = [f"{row}{chr(65 + col)}" for row in range(1, aeronave.fileiras + 1) for col in range(aeronave.assentos_por_fileira)]
        ocupados = voo.assentos
        disponiveis = [assento for assento in total_assentos if assento not in ocupados]
        return disponiveis[0] if disponiveis else None

    def atualizar_assento(self, reserva_cod, novo_assento):
        reserva = self.__dao_reserva.buscar_por_cod(reserva_cod)
        if not reserva:
            return False, "Reserva não encontrada."

        voo = self.__dao_voo.buscar_por_codigo(reserva.voo)
        if not voo:
            return False, "Voo não encontrado."

        if novo_assento in voo.assentos:
            return False, "Assento já ocupado."

        self.__dao_voo.adicionar_assento(voo.cod, novo_assento)
        reserva.assento = novo_assento
        sucesso = self.__dao_reserva.atualizar(reserva)
        if sucesso:
            return True, "Assento atualizado com sucesso."
        else:
            return False, "Erro ao atualizar o assento."
