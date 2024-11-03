from model import Aeronaves
import datetime
from model.Pessoas import Aeromocas, Pilotos

class Voos:
    def __init__(self, cod: str, aeronave: Aeronaves, assentos: dict, origem: str, destino: str, data: datetime.datetime, horario_decolagem: str, pilotos: Pilotos, aeromocas: list):
        self.__cod = cod
        self.__aeronave = aeronave
        self.__assentos = assentos
        self.__origem = origem
        self.__destino = destino
        self.__data = data
        self.__horario_decolagem = horario_decolagem
        self.__pilotos = pilotos
        self.__aeromocas = aeromocas

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
        if isinstance(new_aeronave, Aeronaves):
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
        if isinstance(new_data, datetime.datetime):
            self.__data = new_data

    @property
    def horario_decolagem(self):
        return self.__horario_decolagem
    
    @horario_decolagem.setter
    def horario_decolagem(self, new_horario):
        if isinstance(new_horario, str):
            self.__horario_decolagem = new_horario

    @property
    def pilotos(self):
        return self.__pilotos
    
    @pilotos.setter
    def pilotos(self, new_piloto):
        if isinstance(new_piloto, Pilotos):
            self.__pilotos = new_piloto

    @property
    def aeromocas(self):
        return self.__aeromocas
    
    @aeromocas.setter
    def aeromocas(self, new_aeromoca):
        if isinstance(new_aeromoca, list) and all(isinstance(a, Aeromocas) for a in new_aeromoca):
            self.__aeromocas = new_aeromoca
