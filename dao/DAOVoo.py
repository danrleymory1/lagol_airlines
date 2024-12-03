from dao.DAO import DAO
from dao.DAOAeronaves import DAOAeronaves
from model.Voos import Voos
from model.Aeronaves import Aeronaves
from model.Pessoas.Pilotos import Pilotos
from model.Pessoas.Aeromocas import Aeromocas
import datetime

class DAOVoo(DAO):
    def __init__(self):
        super().__init__()
        self.dao_aeronave = DAOAeronaves()
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
        try:
            result = self.__collection.update_one(
                {"cod": voo.cod},
                {"$set": self.voo_to_dict(voo)}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar voo: {e}")
            return False

    def atualizar_assentos(self, cod_voo, reserva_cod, assento):
        try:
            voo = self.buscar_por_codigo(cod_voo)
            if not voo:
                print("Voo não encontrado para atualizar assentos.")
                return False

            # Adiciona ou substitui o assento com o código da reserva como chave
            voo.assentos[reserva_cod] = assento

            result = self.__collection.update_one(
                {"cod": cod_voo},
                {"$set": {"assentos": voo.assentos}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar os assentos do voo: {e}")
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

        hora = ""
        if voo.horario_decolagem.hour < 10:
            hora = "0" + str(voo.horario_decolagem.hour)
        else:
            hora = str(voo.horario_decolagem.hour)

        minutos = ""
        if voo.horario_decolagem.minute < 10:
            minutos = "0" + str(voo.horario_decolagem.minute)
        else:
            minutos = str(voo.horario_decolagem.minute)
        horario = hora + ":" + minutos
         
        """Converte um objeto Voos em um dicionário para armazenamento."""
        return {
            "cod": voo.cod,
            "aeronave": voo.aeronave.modelo,
            "assentos": voo.assentos,
            "origem": voo.origem,
            "destino": voo.destino,
            "data": voo.data.isoformat() if isinstance(voo.data, datetime.datetime) else voo.data,
            "piloto": voo.piloto,
            "copiloto": voo.copiloto,
            "aeromoca1": voo.aeromoca1,
            "aeromoca2": voo.aeromoca2,
            "horario_decolagem": horario
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

        aeronave_data = voo_dict['aeronave']
        if isinstance(aeronave_data, dict):  # Caso o valor seja um dicionário
            modelo_nome = aeronave_data['modelo']
        elif isinstance(aeronave_data, str):  # Caso o valor seja uma string
            modelo_nome = aeronave_data
        else:
            raise ValueError("Formato de aeronave inválido no dicionário do voo.")

        aeronave = self.dao_aeronave.buscar_por_modelo(modelo_nome)
        if not aeronave:
            raise ValueError(f"Aeronave não encontrada para o modelo: {modelo_nome}")

        return Voos(
            cod=voo_dict.get('cod', ''),
            aeronave=aeronave,
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


