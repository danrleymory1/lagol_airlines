from model import Voos
from model.Pessoas import Clientes


class Reservas:

    def __init__(self, cod:str, numero_reserva:str, passageiro:Passageiro, voo:Voo, assento:str, quant_bagagem:int):

        self.__cod = cod
        self.__numero_reserva = numero_reserva
        self.__passageiro = passageiro
        self.__voo = voo
        self.__assento = assento
        self.__quant_bagagem = quant_bagagem
        
    @property
    def cod(self):
        return self.__cod
    
    @cod.setter
    def cod(self, new_cod):
        if isinstance(new_cod, str):
            self.__cod = new_cod

    @property
    def numero_reserva(self):
        return self.__numero_reserva
    
    @numero_reserva.setter
    def numero_reserva(self, new_numero_reserva):
        if isinstance(new_numero_reserva, str):
            self.__numero_reserva = new_numero_reserva

    @property
    def passageiro(self):
        return self.__passageiro
    
    @passageiro.setter
    def passageiro(self, new_passageiro):
        if isinstance(new_passageiro, Passageiro):
            self.__passageiro = new_passageiro

    @property
    def voo(self):
        return self.__voo
    
    @voo.setter
    def voo(self, new_voo):
        if isinstance(new_voo, Voo):
            self.__voo = new_voo
        
    @property
    def assento(self):
        return self.__assento
    
    @assento.setter
    def assento(self, new_assento):
        if isinstance(new_assento, str):
            self.__assento = new_assento

    @property
    def quant_bagagem(self):
        return self.__quant_bagagem
    
    @quant_bagagem.setter
    def quant_bagagem(self, new_quant_bagagem):
        if isinstance(new_quant_bagagem, int):
            self.__quant_bagagem = new_quant_bagagem