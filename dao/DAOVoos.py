from dao.DAO import DAO
from model.Voos import Voos
from model.Aeronaves import Aeronaves
from model.Pessoas.Pilotos import Pilotos
from model.Pessoas.Aeromocas import Aeromocas
import datetime

class DAOVoos(DAO):
    def __init__(self):
        super().__init__()
        self.__collection = self.db['voos']  # Collection de voos no banco de dados

    def adicionar(self, voo: Voos):
        try:
            voo.cod = self.get_next_cod("voo_cod")  # Gera o próximo código de voo
            result = self.__collection.insert_one(self.voo_to_dict(voo))
            return result.inserted_id is not None
        except Exception as e:
            print(f"Erro ao adicionar voo: {e}")
            return False

    def buscar_por_codigo(self, cod: str):
        voo_dict = self.__collection.find_one({"cod": cod})
        if voo_dict:
            return self.dict_to_voo(voo_dict)
        return None

    def buscar_todos(self):
        voos = []
        for voo_dict in self.__collection.find():
            voos.append(self.dict_to_voo(voo_dict))
        return voos

    def atualizar(self, voo: Voos):
        try:
            result = self.__collection.update_one(
                {"cod": voo.cod},  # Busca pelo código do voo para atualizar
                {"$set": self.voo_to_dict(voo)}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar voo: {e}")
            return False

    def deletar(self, cod: str):
        try:
            result = self.__collection.delete_one({"cod": cod})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Erro ao deletar voo: {e}")
            return False

    def voo_to_dict(self, voo: Voos):
        """Converte um objeto Voos em um dicionário para armazenamento."""
        return {
            "cod": voo.cod,
            "aeronave": voo.aeronave.to_dict(),
            "assentos": voo.assentos,
            "origem": voo.origem,
            "destino": voo.destino,
            "data": voo.data.isoformat(),
            "piloto": voo.piloto.to_dict(),
            "aeromoca": voo.aeromoca.to_dict()
        }

    def dict_to_voo(self, voo_dict: dict):
        """Converte um dicionário em um objeto Voos."""
        return Voos(
            cod=voo_dict['cod'],
            aeronave=Aeronaves.from_dict(voo_dict['aeronave']),
            assentos=voo_dict['assentos'],
            origem=voo_dict['origem'],
            destino=voo_dict['destino'],
            data=datetime.datetime.fromisoformat(voo_dict['data']),
            piloto=Pilotos.from_dict(voo_dict['piloto']),
            aeromoca=Aeromocas.from_dict(voo_dict['aeromoca'])
        )
    
    def buscar_por_cpf(self, cpf):
        pass
