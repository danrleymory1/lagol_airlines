from dao.DAOAeronaves import DAOAeronaves
from model.ModeloAeronaves import ModeloAeronave
from model.Aeronaves import Aeronaves

class ControladorAeronaves:
    def __init__(self):
        self.__dao = DAOAeronaves()

    def cadastrar_aeronave(self, modelo_nome: str):
        """Cadastra uma nova aeronave no sistema."""
        try:
            # Verifica se o modelo informado existe no enum ModeloAeronave
            modelo = ModeloAeronave[modelo_nome.upper()]
            aeronave = Aeronaves(modelo)

            # Adiciona a aeronave ao banco de dados
            if self.__dao.adicionar(aeronave):
                return True, "Aeronave cadastrada com sucesso!"
            else:
                return False, "Erro ao cadastrar a aeronave."
        except KeyError:
            return False, "Modelo de aeronave inválido."
        except Exception as e:
            return False, f"Erro ao cadastrar aeronave: {e}"

    def listar_aeronaves(self):
        """Lista todas as aeronaves cadastradas."""
        try:
            aeronaves = self.__dao.buscar_todas()
            return aeronaves if aeronaves else []
        except Exception as e:
            print(f"Erro ao listar aeronaves: {e}")
            return []

    def buscar_aeronave_por_modelo(self, modelo_nome: str):
        """Busca uma aeronave pelo modelo."""
        try:
            aeronave = self.__dao.buscar_por_modelo(modelo_nome)
            if aeronave:
                return aeronave
            else:
                return None, "Aeronave não encontrada."
        except Exception as e:
            return None, f"Erro ao buscar aeronave: {e}"

    def atualizar_aeronave(self, modelo_nome: str, novos_dados: dict):
        """Atualiza os dados de uma aeronave pelo modelo."""
        try:
            sucesso = self.__dao.atualizar(modelo_nome, novos_dados)
            if sucesso:
                return True, "Aeronave atualizada com sucesso!"
            else:
                return False, "Erro ao atualizar a aeronave."
        except Exception as e:
            return False, f"Erro ao atualizar aeronave: {e}"

    def deletar_aeronave(self, modelo_nome: str):
        """Deleta uma aeronave pelo modelo."""
        try:
            sucesso = self.__dao.deletar(modelo_nome)
            if sucesso:
                return True, "Aeronave deletada com sucesso!"
            else:
                return False, "Erro ao deletar a aeronave."
        except Exception as e:
            return False, f"Erro ao deletar aeronave: {e}"