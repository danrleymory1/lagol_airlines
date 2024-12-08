from dao.DAO import DAO
from model.Aeronaves import Aeronaves
from model.ModeloAeronaves import ModeloAeronave

class DAOAeronaves(DAO):
    def __init__(self):
        super().__init__()
        self.__collection = self.db['aeronaves']  # Define a coleção no banco de dados

    def adicionar(self, aeronave: Aeronaves):
        """Adiciona uma aeronave ao banco de dados."""
        try:
            dados_aeronave = aeronave.to_dict()
            result = self.__collection.insert_one(dados_aeronave)
            return result.inserted_id is not None
        except Exception as e:
            print(f"Erro ao adicionar aeronave: {e}")
            return False

    def buscar_por_modelo(self, modelo_nome: str):
        """Busca uma aeronave pelo nome do modelo e retorna uma instância de Aeronaves."""
        try:
            aeronave_dict = self.__collection.find_one({"modelo": modelo_nome})
            if aeronave_dict:
                modelo = ModeloAeronave.from_modelo(aeronave_dict["modelo"])
                return Aeronaves(modelo=modelo)
            return None
        except Exception as e:
            print(f"Erro ao buscar aeronave: {e}")
            return None

    def buscar_todas(self):
        """Busca todas as aeronaves no banco de dados."""
        try:
            aeronaves = []
            for aeronave_dict in self.__collection.find():
                modelo_nome = aeronave_dict.get('modelo')  # Obter o modelo do banco
                if modelo_nome:
                    try:
                        # Converte o nome do modelo para o Enum ModeloAeronave
                        modelo = ModeloAeronave.from_modelo(modelo_nome)
                        # Instanciar a aeronave e adicioná-la à lista
                        aeronaves.append(Aeronaves(modelo=modelo))
                    except ValueError:
                        print(f"Modelo inválido ou desconhecido no registro: {modelo_nome}")
                else:
                    print(f"Modelo ausente no registro: {aeronave_dict}")
            return aeronaves
        except Exception as e:
            print(f"Erro ao buscar todas as aeronaves: {e}")
            return []

    def atualizar(self, modelo_nome: str, novos_dados: dict):
        """Atualiza os dados de uma aeronave no banco de dados."""
        try:
            result = self.__collection.update_one(
                {"modelo": modelo_nome},
                {"$set": novos_dados}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar aeronave: {e}")
            return False

    def deletar(self, modelo_nome: str):
        """Deleta uma aeronave do banco de dados pelo nome do modelo."""
        try:
            result = self.__collection.delete_one({"modelo": modelo_nome})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Erro ao deletar aeronave: {e}")
            return False
