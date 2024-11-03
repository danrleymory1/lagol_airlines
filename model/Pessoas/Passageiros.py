from model.Pessoas.Pessoas import Pessoas
from datetime import date


class Passageiros(Pessoas):
    def __init__(self, nome, cpf, data_nascimento:date):
        super().__init__(nome, cpf)
        self.__data_nascimento = data_nascimento

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, nova_data):
        if isinstance(nova_data, date):
            self.__data_nascimento = nova_data

    def to_dict(self):
        pessoa_dict = super().to_dict()
        pessoa_dict.update({
            "data_nascimento": self.__data_nascimento
        })
        return pessoa_dict
