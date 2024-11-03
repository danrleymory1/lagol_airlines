from dao.DAO import DAO
from model.Voos import Voos


class DAOVoo(DAO):
    def __init__(self):
        super().__init__()
        self.__collection = self.db['voos']

    def adicionar(self, voo):
        try:
            voo.cod = self.get_next_cod("voo_cod")
            result = self.__collection.insert_one(voo.to_dict())
            return result.inserted_id is not None
        except Exception as e:
            print(f"Erro ao adicionar o voo: {e}")
            return False

    def buscar_por_cod(self, cod):
        voo_dict = self.__collection.find_one({"cod": cod})

        if voo_dict:
            return Voos(
                aeromocas=voo_dict['aeromocas'],
                aeronave=voo_dict['aeronave'],
                assentos=voo_dict['assentos'],
                data=voo_dict['data'],
                destino=voo_dict['destino'],
                horario_decolagem=voo_dict['horario_decolagem'],
                origem=voo_dict['origem'],
                pilotos=voo_dict['pilotos']
            )
        return None


    def buscar_voos(self, filtros):
        voos_dict = self.__collection.find(filtros)
        voos = []

        if voos_dict:
            for voos in voos_dict:
                voo = Voos(
                    aeromocas=voos['aeromocas'],
                    aeronave=voos['aeronave'],
                    assentos=voos['assentos'],
                    data=voos['data'],
                    destino=voos['destino'],
                    horario_decolagem=voos['horario_decolagem'],
                    origem=voos['origem'],
                    pilotos=voos['pilotos']
                )
            return voos
        return None

    def atualizar(self, voo):
        try:
            result = self.__collection.update_one(
                {"cod": voo.cod},
                {"$set": {
                    
                    "aeromocas": voo.aeromocas,
                    "aeronave": voo.aeronave,
                    "assentos": voo.assentos,
                    "data": voo.data,
                    "destino": voo.destino,
                    "horario_decolagem": voo.horario_decolagem,
                    "origem": voo.origem,
                    "pilotos": voo.pilotos
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar voo: {e}")
            return False

    def deletar(self, cod):
        try:
            result = self.__collection.delete_one({"cod": cod})
            return result.deleted_count > 0  # Retorna True se um documento foi deletado
        except Exception as e:
            print(f"Erro ao deletar voo: {e}")
            return False