from model.ModeloAeronaves import ModeloAeronave


class Aeronaves():

    def __init__(self, modelo:ModeloAeronave):
        self.__modelo = modelo
        self.__cod = None
        
    @property
    def modelo(self):
        return self.__modelo

    @modelo.setter
    def modelo(self, novo_modelo):
        if isinstance(novo_modelo, ModeloAeronave):
            self.__modelo = novo_modelo
    
    @property
    def codigo(self):
        return self.__cod

    @codigo.setter
    def codigo(self, novo_cod):
        if isinstance(novo_cod, int):
            self.__codigo = novo_cod


