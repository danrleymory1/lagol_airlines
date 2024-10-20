from model.ModeloAeronaves import ModeloAeronave


class Aeronaves():

    def __init__(self, modelo:ModeloAeronave, voos:list):
        self.__modelo = modelo
        self.__voos = voos
        
    @property
    def modelo(self):
        return self.__modelo

    @modelo.setter
    def modelo(self, nova_data):
        if isinstance(nova_data, ModeloAeronave):
            self.__modelo = nova_data

    @property
    def voos(self):
        return self.__voos

    @voos.setter
    def voos(self, nova_data):
        if isinstance(nova_data, list):
            self.__voos = nova_data