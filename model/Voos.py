from model import Aeronaves
import datetime

from model.Pessoas import Aeromocas, Pilotos

class Voos:

    def __init__(self, cod:str, aeronave:Aeronave, assentos:dict, origem:str, destino:str, data:datetime, piloto:Piloto, aeromoca:Aeromoca):
        self.__cod = cod
        self.__aeronave = aeronave
        self.__assentos = assentos
        self.__origem = origem
        self.__destino = destino
        self.__data = data
        self.__piloto = piloto
        self.__aeromoca = aeromoca

    @property
    def cod(self):
        return self.__cod
    
    @cod.setter
    def cod(self, new_cod):
        if isinstance(new_cod, str):
            self.__cod = new_cod

    @property
    def aeronave(self):
        return self.__aeronave
    
    @aeronave.setter
    def aeronave(self, new_aeronave):
        if isinstance(new_aeronave, Aeronave):
            self.__aeronave = new_aeronave

    @property
    def assentos(self):
        return self.__assentos
    
    @assentos.setter
    def assentos(self, new_assentos):
        if isinstance(new_assentos, dict):
            self.__assentos = new_assentos

    @property
    def origem(self):
        return self.__origem
    
    @origem.setter
    def origem(self, new_origem):
        if isinstance(new_origem, str):
            self.__origem = new_origem

    @property
    def destino(self):
        return self.__destino
    
    @destino.setter
    def destino(self, new_destino):
        if isinstance(new_destino, str):
            self.__destino = new_destino

    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, new_data):
        if isinstance(new_data, datetime):
            self.__data = new_data
    
    @property
    def piloto(self):
        return self.__piloto
    
    @piloto.setter
    def piloto(self, new_piloto):
        if isinstance(new_piloto, Piloto):
            self.__piloto = new_piloto

    @property
    def aeromoca(self):
        return self.__aeromoca
    
    @aeromoca.setter
    def aeromoca(self, new_aeromoca):
        if isinstance(new_aeromoca, Aeromoca):
            self.__aeromoca = new_aeromoca