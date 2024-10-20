from dao.DAO import DAO

class DAOAdminLogin(DAO):
    def __init__(self):
        super().__init__()
        self.__collection = self.db['admins']

    def adicionar(self, admin):
        pass

    def buscar_por_cpf(self, cpf):
        return self.__collection.find_one({"cpf": cpf})