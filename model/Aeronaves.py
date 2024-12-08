from model.ModeloAeronaves import ModeloAeronave


class Aeronaves:
    def __init__(self, modelo: ModeloAeronave):
        if not isinstance(modelo, ModeloAeronave):
            raise ValueError("O modelo deve ser uma instância de ModeloAeronave.")

        self.__modelo = modelo
        self.__fileiras = modelo.fileiras
        self.__assentos_por_fileira = modelo.assentos_por_fileira
        self.__max_bagagens = modelo.max_bagagens
        self.__voos = []

    @property
    def modelo(self):
        return self.__modelo

    @property
    def fileiras(self):
        return self.__fileiras

    @property
    def assentos_por_fileira(self):
        return self.__assentos_por_fileira

    @property
    def max_bagagens(self):
        return self.__max_bagagens

    @property
    def voos(self):
        return self.__voos

    def adicionar_voo(self, voo):
        if voo not in self.__voos:
            self.__voos.append(voo)

    def remover_voo(self, voo):
        if voo in self.__voos:
            self.__voos.remove(voo)

    def to_dict(self):
        return {
            "modelo": self.__modelo.name,
            "fileiras": self.__fileiras,
            "assentos_por_fileira": self.__assentos_por_fileira,
            "max_bagagens": self.__max_bagagens,
            "voos": [voo.to_dict() for voo in self.__voos]
        }

    def __str__(self):
        return self.__modelo.name
