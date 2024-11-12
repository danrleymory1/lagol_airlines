from model import Voos
from model.Pessoas import Clientes, Passageiros


class Reservas:

    def __init__(self, cod:str, cliente:Clientes, passageiro:Passageiros, voo:Voos, assento:str):

        self.__cod = cod
        self.__cliente = cliente
        self.__passageiro = passageiro
        self.__voo = voo
        self.__assento = assento
        self.__quant_bagagem = 1
        self.__pagamento_extra_assento = False
        self.__compareceu = False
        
    @property
    def cod(self):
        return self.__cod
    
    @cod.setter
    def cod(self, new_cod):
        if isinstance(new_cod, str):
            self.__cod = new_cod

    @property
    def passageiro(self):
        return self.__passageiro
    
    @passageiro.setter
    def passageiro(self, new_passageiro):
        if isinstance(new_passageiro, Passageiros):
            self.__passageiro = new_passageiro

    @property
    def cliente(self):
        return self.__cliente
    
    @cliente.setter
    def cliente(self, new_cliente):
        if isinstance(new_cliente, Clientes):
            self.__cliente = new_cliente

    @property
    def voo(self):
        return self.__voo
    
    @voo.setter
    def voo(self, new_voo):
        if isinstance(new_voo, Voos):
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

    @property
    def pagamento_extra_assento(self):
        return self.__pagamento_extra_assento
    
    @pagamento_extra_assento.setter
    def pagamento_extra_assento(self, new_pagamento_extra_assento):
        if isinstance(new_pagamento_extra_assento, bool):
            self.__pagamento_extra_assento = new_pagamento_extra_assento
    
    @property
    def compareceu(self):
        return self.__compareceu
    
    @compareceu.setter
    def compareceu(self, new_compareceu):
        if isinstance(new_compareceu, bool):
            self.__compareceu = new_compareceu