from enum import Enum

class ModeloAeronave(Enum):
    BOING_737 = {"nome": "Boing 737", "fileiras": 30, "assentos_por_fileira": 6,
                 "max_bagagens": int(30 * 6 * 1.5)}
    AIRBUS_A220 = {"nome": "Airbus A220", "fileiras": 25, "assentos_por_fileira": 6,
                   "max_bagagens": int(25 * 6 * 1.5)}
    EMBRAER_190 = {"nome": "Embraer 190", "fileiras": 20, "assentos_por_fileira": 4,
                   "max_bagagens": int(20 * 4 * 1.5)}

    @property
    def nome(self):
        return self.value["nome"]

    @property
    def fileiras(self):
        return self.value["fileiras"]

    @property
    def assentos_por_fileira(self):
        return self.value["assentos_por_fileira"]

    @property
    def max_bagagens(self):
        return self.value["max_bagagens"]
