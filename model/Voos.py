from model import Aeronaves
import datetime
from model.Pessoas import Aeromocas, Pilotos

class Voos:
    def __init__(self, cod: str, aeronave: Aeronaves, assentos: list, origem: str, destino: str, data: datetime.datetime,
                 horario_decolagem: str, piloto: Pilotos, copiloto: Pilotos, aeromoca1: Aeromocas, aeromoca2: Aeromocas):
        self.__cod = cod
        self.__aeronave = aeronave
        self.__assentos = assentos
        self.__origem = origem
        self.__destino = destino
        self.__data = data
        self.__horario_decolagem = horario_decolagem
        self.__piloto = piloto
        self.__copiloto = copiloto
        self.__aeromoca1 = aeromoca1
        self.__aeromoca2 = aeromoca2
      

    # Propriedades e validadores

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
        if isinstance(new_aeronave, str):
            self.__aeronave = new_aeronave

    @property
    def assentos(self):
        return self.__assentos
    
    @assentos.setter
    def assentos(self, new_assentos):
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
        self.__horario_decolagem = new_horario

    @property
    def piloto(self):
        return self.__piloto
    
    @piloto.setter
    def piloto(self, new_piloto):
        self.__piloto = new_piloto

    @property
    def copiloto(self):
        return self.__copiloto
    
    @copiloto.setter
    def copiloto(self, new_copiloto):
        self.__copiloto = new_copiloto

    @property
    def aeromoca1(self):
        return self.__aeromoca1
    
    @aeromoca1.setter
    def aeromoca1(self, new_aeromoca1):
        self.__aeromoca1 = new_aeromoca1

    @property
    def aeromoca2(self):
        return self.__aeromoca2
    
    @aeromoca2.setter
    def aeromoca2(self, new_aeromoca2):
        self.__aeromoca2 = new_aeromoca2
    

    def __gerar_assentos(self):
        """Gera a lista de dicionários com os assentos disponíveis."""
        assentos = []
        for fileira in range(1, self.__aeronave.fileiras + 1):
            for coluna in range(self.__aeronave.assentos_por_fileira):
                assento = f"{fileira}{chr(65 + coluna)}"
                assentos.append({assento: None})
        return assentos
