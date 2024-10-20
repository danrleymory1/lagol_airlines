from abc import ABC

class Pessoas(ABC):
    def __init__(self, nome, cpf):
        self.__cod = None
        self.__nome = nome
        self.__cpf = cpf

    @property
    def cod(self):
        return self.__cod

    @cod.setter
    def cod(self, value):
        self.__cod = value

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = value

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, value):
        self.__cpf = value

    def to_dict(self):
        return {
            "cod": self.__cod,
            "nome": self.__nome,
            "cpf": self.__cpf
        }
