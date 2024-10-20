from Pessoas import Pessoas

class Admins(Pessoas):
    def __init__(self, nome, cpf, senha):
        super().__init__(nome, cpf)
        self.__senha = None
        self.senha = senha

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha  # Assume it's already hashed

    def to_dict(self):
        pessoa_dict = super().to_dict()
        pessoa_dict.update({
            "senha": self.__senha,
        })
        return pessoa_dict