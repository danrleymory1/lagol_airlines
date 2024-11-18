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
        #print(f"Buscando voo com código: {cod} (tipo: {type(cod)})")
        voo_dict = self.__collection.find_one({"cod": int(cod)})  # Converte 'cod' para inteiro
        #print(f"Resultado da busca no banco: {voo_dict}")
        if voo_dict:
            voo = self.dict_to_voo(voo_dict)
            #print(f"Objeto convertido: {voo}")
            return voo
        print("Nenhum voo encontrado.")
        return None



    def buscar_voos(self):
        voos_dict = self.__collection.find()
        voos_list = []
        for voo_dict in voos_dict:
            voos_list.append(self.dict_to_voo(voo_dict))
        return voos_list

    def atualizar(self, voo: Voos):
        print('BBBBBBBBBBBBBBB')
        print(self.voo_to_dict(voo))
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
            print(cod)
            print(f"Usando a coleção: {self.__collection.name}")
            result = self.__collection.delete_one(
                {"cod": int(cod)})
            print(result)
            print(result.deleted_count)
            return result.deleted_count > 0
        except Exception as e:
            print(f"Erro ao deletar voo: {e}")
            return False

    def voo_to_dict(self, voo: Voos):
        print("AAAAAAAAAAAAAAAAAA")
     
        """Converte um objeto Voos em um dicionário para armazenamento."""
        return {
            "cod": voo.cod,
            "aeronave": voo.aeronave.to_dict() if isinstance(voo.aeronave, Aeronaves) else voo.aeronave,
            "assentos": voo.assentos,
            "origem": voo.origem,
            "destino": voo.destino,
            "data": voo.data.isoformat() if isinstance(voo.data, datetime.datetime) else voo.data,
            "piloto": voo.piloto,
            "copiloto": voo.copiloto,
            "aeromoca1": voo.aeromoca1,
            "aeromoca2": voo.aeromoca2,
            "horario_decolagem": str(voo.horario_decolagem.hour) + ":" + str(voo.horario_decolagem.minute)
        }

    def dict_to_voo(self, voo_dict: dict):
        """Converte um dicionário em um objeto Voos."""
        horario_decolagem = voo_dict.get('horario_decolagem', '')

        # Se o horario_decolagem for um número (em minutos), converte para o formato HH:MM
        if isinstance(horario_decolagem, int):
            horas = horario_decolagem // 60
            minutos = horario_decolagem % 60
            horario_decolagem = f"{horas:02d}:{minutos:02d}"

        # Se o horario_decolagem for uma string no formato HH:MM, mantemos como está
        elif isinstance(horario_decolagem, str) and len(horario_decolagem) == 5:
            pass  # Mantém a string como está se já estiver no formato correto

        return Voos(
            cod=voo_dict.get('cod', ''),
            aeronave=Aeronaves.from_dict(voo_dict['aeronave']) if isinstance(voo_dict.get('aeronave'), dict) else voo_dict.get('aeronave'),
            assentos=voo_dict.get('assentos', {}),
            origem=voo_dict.get('origem', ''),
            destino=voo_dict.get('destino', ''),
            data=datetime.datetime.fromisoformat(voo_dict.get('data', '1970-01-01T00:00:00')) if isinstance(voo_dict.get('data'), str) else voo_dict.get('data'),
            horario_decolagem=horario_decolagem,  # Já convertido ou mantido como está
            piloto=Pilotos.from_dict(voo_dict['piloto']) if isinstance(voo_dict.get('piloto'), dict) else voo_dict.get('piloto'),
            copiloto=Pilotos.from_dict(voo_dict.get('copiloto')) if isinstance(voo_dict.get('copiloto'), dict) else voo_dict.get('copiloto'),
            aeromoca1=Aeromocas.from_dict(voo_dict.get('aeromoca1')) if isinstance(voo_dict.get('aeromoca1'), dict) else voo_dict.get('aeromoca1'),
            aeromoca2=Aeromocas.from_dict(voo_dict.get('aeromoca2')) if isinstance(voo_dict.get('aeromoca2'), dict) else voo_dict.get('aeromoca2')
        )


