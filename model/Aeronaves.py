from model.ModeloAeronaves import ModeloAeronave

class Aeronaves:

    def __init__(self, modelo: ModeloAeronave):
        if not isinstance(modelo, ModeloAeronave):
            raise ValueError("O modelo deve ser uma instância da classe ModeloAeronave.")
        
        # Atributos definidos com base no modelo selecionado
        self.__modelo = modelo
        self.__fileiras = modelo.fileiras
        self.__assentos_por_fileira = modelo.assentos_por_fileira
        self.__max_bagagens = modelo.max_bagagens
        self.__voos = []  # Inicialmente sem voos associados

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
        """Adiciona um voo à lista de voos associados à aeronave."""
        if voo not in self.__voos:
            self.__voos.append(voo)

    def remover_voo(self, voo):
        """Remove um voo da lista de voos associados à aeronave."""
        if voo in self.__voos:
            self.__voos.remove(voo)

    def to_dict(self):
        """Converte os dados da aeronave para um dicionário."""
        return {
            "modelo": self.__modelo.nome,
            "fileiras": self.__fileiras,
            "assentos_por_fileira": self.__assentos_por_fileira,
            "max_bagagens": self.__max_bagagens,
            "voos": [voo.to_dict() for voo in self.__voos] 
        }
