from model.Reservas import Reservas
from dao.DAOReserva import DAOReserva
import random
import string


class ControladorReserva:
    def __init__(self):
        self.__dao = DAOReserva()

    def cadastrar_reserva(self, passageiro, cliente, voo_cod):

        while(True):
            cod = random.choices(string.digits+string.ascii_uppercase, k=5)
            if self.validar_codigo(cod):
                break
        
        assento = str(random.randint(1, 30)) + random.choice("ABCDEF") #todo: verificar se o assento já está ocupado

        reserva = Reservas(cod=cod, passageiro=passageiro, cliente=cliente, voo=voo_cod, assento=assento)

        if self.__dao.adicionar(reserva):
            return True, "Reserva realizada com sucesso!"
        else:
            return False, "Erro ao cadastrar a reserva. Tente novamente."
        
    def validar_codigo(self, cod):
        if self.__dao.buscar_por_cod(cod):
            return False
        return True

    def buscar_reserva_por_cod(self, cod):
        return self.__dao.buscar_por_cod(cod)

    def deletar_reserva(self, cod):
        sucesso = self.__dao.deletar(cod)
        if sucesso:
            return True, "Reserva deletada com sucesso!"
        else:
            return False, "Erro ao deletar reserva. Tente novamente."

