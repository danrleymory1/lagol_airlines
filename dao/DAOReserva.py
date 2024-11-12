from dao.DAO import DAO
from model.Reservas import Reservas


class DAOReserva(DAO):
    def __init__(self):
        super().__init__()
        self.__collection = self.db['reservas']

    def adicionar(self, reserva):
        print(reserva)
        print(reserva.to_dict())
        try:
            result = self.__collection.insert_one(reserva.to_dict())
            return result.inserted_id is not None
        except Exception as e:
            print(f"Erro ao adicionar a reserva: {e}")
            return False

    def buscar_por_cod(self, cod):

        reserva_dict = self.__collection.find_one({"cod": cod})

        if reserva_dict:
            return Reservas(
                cod=reserva_dict['cod'],
                aeromocas=reserva_dict['aeromocas'],
                aeronave=reserva_dict['aeronave'],
                assentos=reserva_dict['assentos'],
                data=reserva_dict['data'],
                destino=reserva_dict['destino'],
                horario_decolagem=reserva_dict['horario_decolagem'],
                origem=reserva_dict['origem'],
                pilotos=reserva_dict['pilotos']
            )
        return None



    def buscar_reservas(self, filtros):
        reservas_dict = self.__collection.find(filtros)
        reservas_list = []

        if reservas_dict:
            for reservas in reservas_dict:
                reserva = Reservas(
                    cod=reservas['cod'],
                    aeromocas=reservas['aeromocas'],
                    aeronave=reservas['aeronave'],
                    assentos=reservas['assentos'],
                    data=reservas['data'],
                    destino=reservas['destino'],
                    horario_decolagem=reservas['horario_decolagem'],
                    origem=reservas['origem'],
                    pilotos=reservas['pilotos']
                )
                reservas_list.append(reserva)
            return reservas_list
        return None

    def atualizar(self, reserva):
        try:
            result = self.__collection.update_one(
                {"cod": reserva.cod},
                {"$set": {
                    "aeromocas": reserva.aeromocas,
                    "aeronave": reserva.aeronave,
                    "assentos": reserva.assentos,
                    "data": reserva.data,
                    "destino": reserva.destino,
                    "horario_decolagem": reserva.horario_decolagem,
                    "origem": reserva.origem,
                    "pilotos": reserva.pilotos
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar reserva: {e}")
            return False

    def deletar(self, cod):
        try:
            result = self.__collection.delete_one({"cod": cod})
            return result.deleted_count > 0  # Retorna True se um documento foi deletado
        except Exception as e:
            print(f"Erro ao deletar reserva: {e}")
            return False