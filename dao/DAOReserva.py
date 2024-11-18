from dao.DAO import DAO
from model.Reservas import Reservas


class DAOReserva(DAO):
    def __init__(self):
        super().__init__()
        self.__collection = self.db['reservas']

    def adicionar(self, reserva):
       
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
                passageiro=reserva_dict['passageiro'],
                cliente=reserva_dict['cliente'],
                voo=reserva_dict['voo'],
                assento=reserva_dict['assento'], 
            )
        return None


    def buscar_reservas(self, filtros):
        print(filtros)
        reservas_dict = self.__collection.find(filtros)
        print(f"Reservas dict encontradas {reservas_dict}")
        reservas_list = []

        if reservas_dict:
            for reserva in reservas_dict:
                print(reserva)
                reserva = Reservas(
                    cod=reserva['cod'],
                    passageiro=reserva['passageiro'],
                    cliente=reserva['cliente'],
                    voo=reserva['voo'],
                    assento=reserva['assento'], 
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

    def atualizar_assento(self, reserva_cod, novo_assento):
        try:
            result = self.__collection.update_one(
                {"cod": reserva_cod},
                {"$set": {"assento": novo_assento}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar assento da reserva: {e}")
            return False

    def deletar(self, cod):
        try:
            result = self.__collection.delete_one({"cod": cod})
            return result.deleted_count > 0  # Retorna True se um documento foi deletado
        except Exception as e:
            print(f"Erro ao deletar reserva: {e}")
            return False