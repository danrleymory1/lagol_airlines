from enum import Enum

class ModeloAeronave(Enum):
    BOING_737 = {"fileiras": 30, "assentos_por_fileira": 6, "max_bagagens": int(30 * 6 * 1.5)}
    AIRBUS_A220 = {"fileiras": 25, "assentos_por_fileira": 6, "max_bagagens": int(25 * 6 * 1.5)}
    EMBRAER_190 = {"fileiras": 20, "assentos_por_fileira": 4, "max_bagagens": int(20 * 4 * 1.5)}
    PARA_TESTE = {"fileiras": 4, "assentos_por_fileira": 2, "max_bagagens": int(4 * 2 * 1.5)}

    @property
    def fileiras(self):
        return self.value["fileiras"]

    @property
    def assentos_por_fileira(self):
        return self.value["assentos_por_fileira"]

    @property
    def max_bagagens(self):
        return self.value["max_bagagens"]

    @classmethod
    def from_modelo(cls, modelo: str):
        """Busca o enum correspondente pelo nome do modelo."""
        modelo_formatado = modelo.replace(" ", "_").upper()
        if modelo_formatado in cls.__members__:
            return cls[modelo_formatado]
        raise ValueError(f"Modelo de aeronave desconhecido: {modelo}")
