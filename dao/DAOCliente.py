from dao.DAO import DAO
from model.Pessoas.Clientes import Clientes


class DAOCliente(DAO):
    def __init__(self):
        super().__init__()
        self.__collection = self.db['clientes']

    def adicionar(self, cliente):
        try:
            cliente.cod = self.get_next_cod("cliente_cod")
            result = self.__collection.insert_one(cliente.to_dict())
            return result.inserted_id is not None
        except Exception as e:
            print(f"Erro ao adicionar o cliente: {e}")
            return False

    def buscar_por_cpf(self, cpf):
        cliente_dict = self.__collection.find_one({"cpf": cpf})

        if cliente_dict:
            return Clientes(
                nome=cliente_dict['nome'],
                cpf=cliente_dict['cpf'],
                data_nascimento=cliente_dict['data_nascimento'],
                senha=cliente_dict['senha']
            )
        return None

    def atualizar(self, cliente):
        try:
            result = self.__collection.update_one(
                {"cpf": cliente.cpf},
                {"$set": {
                    "nome": cliente.nome,
                    "data_nascimento": cliente.data_nascimento,
                    "senha": cliente.senha
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")
            return False

    def deletar(self, cpf):
        try:
            result = self.__collection.delete_one({"cpf": cpf})
            return result.deleted_count > 0  # Retorna True se um documento foi deletado
        except Exception as e:
            print(f"Erro ao deletar cliente: {e}")
            return False