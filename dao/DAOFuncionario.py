from dao.DAO import DAO
from model.Pessoas.Funcionarios import Funcionarios

class DAOFuncionario(DAO):
    def __init__(self):
        super().__init__()
        self.__collection = self.db['funcionarios']

    def adicionar(self, funcionario):
        try:
            funcionario.cod = self.get_next_cod("funcionario_cod")
            result = self.__collection.insert_one(funcionario.to_dict())
            return result.inserted_id is not None
        except Exception as e:
            print(f"Erro ao adicionar funcionário: {e}")
            return False

    def buscar_por_cpf(self, cpf):
        print("==============================================")
        print(cpf)
        funcionario_dict = self.__collection.find_one({"cpf": cpf})
        if funcionario_dict:
            return Funcionarios(
                nome=funcionario_dict['nome'],
                cpf=funcionario_dict['cpf'],
                cargo=funcionario_dict['cargo']
            )
        return None

    def buscar_todos(self):
        funcionarios = []
        for funcionario_dict in self.__collection.find():
            funcionarios.append(Funcionarios(
                nome=funcionario_dict['nome'],
                cpf=funcionario_dict['cpf'],
                cargo=funcionario_dict['cargo']
            ))
        return funcionarios

    def atualizar(self, funcionario):

        try:
            result = self.__collection.update_one(
                {"cpf": funcionario.cpf},  # Usa o CPF como identificador
                {"$set": {"nome": funcionario.nome, "cargo": funcionario.cargo}}  # Atualiza os campos desejados
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar o funcionário: {e}")
            return False

    def deletar(self, cpf):
        try:
            result = self.__collection.delete_one({"cpf": cpf})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Erro ao deletar funcionário: {e}")
            return False