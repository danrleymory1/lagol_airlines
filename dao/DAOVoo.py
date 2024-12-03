from dao.DAO import DAO
from dao.DAOAeronaves import DAOAeronaves
from model.Voos import Voos
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
        """Busca um voo pelo código."""
        try:
            voo_dict = self.__collection.find_one({"cod": int(cod)})
            if voo_dict:
                return self.dict_to_voo(voo_dict)
            print(f"Nenhum voo encontrado com código: {cod}")
            return None
        except Exception as e:
            print(f"Erro ao buscar voo por código: {e}")
            return None

    def buscar_voos(self):
        """Busca todos os voos."""
        try:
            voos_dict = self.__collection.find()
            return [self.dict_to_voo(voo_dict) for voo_dict in voos_dict]
        except Exception as e:
            print(f"Erro ao buscar todos os voos: {e}")
            return []

    def atualizar(self, voo: Voos):
        """Atualiza um voo no banco de dados."""
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
        """Atualiza os assentos de um voo."""
        try:
            voo = self.buscar_por_codigo(cod_voo)
            if not voo:
                print("Voo não encontrado para atualizar assentos.")
                return False

            # Adiciona ou substitui o assento com o código da reserva como chave
            voo.assentos[assento] = reserva_cod

            result = self.__collection.update_one(
                {"cod": cod_voo},
                {"$set": {"assentos": voo.assentos}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar os assentos do voo: {e}")
            return False

    def deletar(self, cod: str):
        """Deleta um voo pelo código."""
        try:
            result = self.__collection.delete_one({"cod": int(cod)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Erro ao deletar voo: {e}")
            return False

    def voo_to_dict(self, voo: Voos):
        """Converte um objeto Voos em um dicionário para armazenamento."""
        return {
            "cod": voo.cod,
            "aeronave": voo.aeronave.modelo.name,  # Armazena apenas o nome do modelo da aeronave
            "assentos": voo.assentos,
            "origem": voo.origem,
            "destino": voo.destino,
            "data": voo.data.isoformat() if isinstance(voo.data, datetime.datetime) else voo.data,
            "horario_decolagem": voo.horario_decolagem.strftime("%H:%M") if voo.horario_decolagem else None,
            "piloto": voo.piloto,
            "copiloto": voo.copiloto,
            "aeromoca1": voo.aeromoca1,
            "aeromoca2": voo.aeromoca2,
        }

    def dict_to_voo(self, voo_dict):
        """Converte um dicionário armazenado no banco em um objeto Voos."""
        try:
            # Verificar se já é um objeto do tipo Voos
            if isinstance(voo_dict, Voos):
                print("Objeto Voos já fornecido, retornando diretamente.")
                return voo_dict

            if not isinstance(voo_dict, dict):
                raise ValueError(f"O objeto fornecido não é um dicionário válido: {voo_dict}")

            horario_decolagem = voo_dict.get('horario_decolagem', '')

            # Converter horário de decolagem para datetime.time
            if isinstance(horario_decolagem, str) and len(horario_decolagem) == 5:
                horario_decolagem = datetime.datetime.strptime(horario_decolagem, '%H:%M').time()

            # Buscar a aeronave associada
            modelo_nome = voo_dict['aeronave']
            aeronave = self.dao_aeronave.buscar_por_modelo(modelo_nome)
            if not aeronave:
                raise ValueError(f"Aeronave não encontrada para o modelo: {modelo_nome}")

            return Voos(
                cod=voo_dict.get('cod', ''),
                aeronave=aeronave,
                assentos=voo_dict.get('assentos', []),
                origem=voo_dict.get('origem', ''),
                destino=voo_dict.get('destino', ''),
                data=datetime.datetime.fromisoformat(voo_dict.get('data')) if isinstance(voo_dict.get('data'),
                                                                                         str) else voo_dict.get('data'),
                horario_decolagem=horario_decolagem,
                piloto=voo_dict.get('piloto'),
                copiloto=voo_dict.get('copiloto'),
                aeromoca1=voo_dict.get('aeromoca1'),
                aeromoca2=voo_dict.get('aeromoca2'),
            )
        except Exception as e:
            print(f"Erro ao converter dicionário para objeto Voos: {e}")
            return None

