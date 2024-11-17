from dao.DAO import DAO
from model.Voos import Voos
from model.Aeronaves import Aeronaves
from model.Pessoas.Pilotos import Pilotos
from model.Pessoas.Aeromocas import Aeromocas
import datetime

class DAOVoo(DAO):
    def __init__(self):
        super().__init__()
        self.__collection = self.db['voos']  # Collection de voos no banco de dados

    def adicionar(self, voo: Voos):
        try:
            result = self.__collection.insert_one(self.voo_to_dict(voo))
            return result.inserted_id is not None
        except Exception as e:
            print(f"Erro ao adicionar voo: {e}")
            return False

    def buscar_por_codigo(self, cod):
        voo_dict = self.__collection.find_one({"cod": cod})
        if voo_dict:
            return self.dict_to_voo(voo_dict)
        return None

    def buscar_voos(self):
        voos_dict = self.__collection.find()
        voos_list = []
        for voo_dict in voos_dict:
            voos_list.append(self.dict_to_voo(voo_dict))
        return voos_list

    def atualizar(self, voo: Voos):
        try:
            result = self.__collection.update_one(
                {"cod": voo.cod},
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
            "aeronave": voo.aeronave.to_dict() if isinstance(voo.aeronave, Aeronaves) else voo.aeronave,
            "assentos": voo.assentos,
            "origem": voo.origem,
            "destino": voo.destino,
            "data": voo.data.isoformat() if isinstance(voo.data, datetime.datetime) else voo.data,
            "pilotos": [piloto.to_dict() for piloto in voo.pilotos] if isinstance(voo.pilotos, list) else voo.pilotos,
            "aeromocas": [aeromoca.to_dict() for aeromoca in voo.aeromocas] if isinstance(voo.aeromocas, list) else voo.aeromocas,
            "horario_decolagem": voo.horario_decolagem if hasattr(voo, 'horario_decolagem') else None
        }

def dict_to_voo(self, voo_dict: dict):
    """Converte um dicionário em um objeto Voos."""
    return Voos(
        cod=voo_dict.get('cod', ''),  # Se não houver, retorna uma string vazia
        aeronave=Aeronaves.from_dict(voo_dict['aeronave']) if isinstance(voo_dict.get('aeronave'), dict) else voo_dict.get('aeronave'),
        assentos=voo_dict.get('assentos', {}),  # Se não houver, retorna um dicionário vazio
        origem=voo_dict.get('origem', ''),
        destino=voo_dict.get('destino', ''),
        data=datetime.datetime.fromisoformat(voo_dict.get('data', '1970-01-01T00:00:00')) if isinstance(voo_dict.get('data'), str) else voo_dict.get('data'),
        horario_decolagem=voo_dict.get('horario_decolagem', ''),
        piloto=Pilotos.from_dict(voo_dict['piloto']) if isinstance(voo_dict.get('piloto'), dict) else voo_dict.get('piloto'),
        copiloto=Pilotos.from_dict(voo_dict.get('copiloto')) if isinstance(voo_dict.get('copiloto'), dict) else voo_dict.get('copiloto'),
        aeromoca1=Aeromocas.from_dict(voo_dict.get('aeromoca1')) if isinstance(voo_dict.get('aeromoca1'), dict) else voo_dict.get('aeromoca1'),
        aeromoca2=Aeromocas.from_dict(voo_dict.get('aeromoca2')) if isinstance(voo_dict.get('aeromoca2'), dict) else voo_dict.get('aeromoca2')
    )

