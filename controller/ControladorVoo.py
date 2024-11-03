
from dao.DAOVoo import DAOVoos
from model.Aeronaves import Aeronaves
from model.Voos import Voos

class ControladorVoos:
    def __init__(self):
        self.__dao = DAOVoos()

    def cadastrar_Voos(self, origem, destino, aeromocas, pilotos, data, horario, aeronave, assentos):
        if not origem:
            return False, "Adicione uma origem."
        
        if not isinstance(origem, str):
            return False, "Erro: Origem tem que ser uma string."
        
        if not destino:
            return False, "Adicione um destino."
        
        if not isinstance(destino, str):
            return False, "Erro: Destino tem que ser uma string"
        
        if not aeromocas:
            return False, "Adicione as aeromoças."
        
        if not isinstance(aeromocas, list):
            return False, "Erro: Aeromoças deve ser uma lista."
        
        if not pilotos:
            return False, "Adicione os pilotos."
        
        if not isinstance(aeromocas, list):
            return False, "Erro: Aeromoças deve ser uma lista."
        
        if not data:
            return False, "Adicione uma data."
        
        if not horario:
            return False, "Adicione um horario."
        
        if not aeronave:
            return False, "Adicione uma aeronave."
        
        if not isinstance(aeronave, Aeronaves):
            return False, "Erro: Aeronave deve ser uma instancia da classe Aeronaves."
        
        if not assentos:
            return False, "Adicione os assentos."

        Voo = Voos(origem=origem, destino=destino, aeromoca=aeromocas, piloto=pilotos, data=data, horario=horario, aeronave=aeronave, assentos=assentos)

        if self.__dao.adicionar(Voo):
            return True, "Cadastro do voo realizado com sucesso!"
        else:
            return False, "Erro ao cadastrar o voo. Tente novamente."

    def buscar_todos_Voos(self):
        return self.__dao.buscar_todos()

    def buscar_Voos(self, filtros):
        return self.__dao.buscar_por_cpf(filtros)

    def alterar_Voo(self, cod, novo_nome): 
        Voos = self.__dao.buscar_por_cod(cod)
        if not Voos:
            return False, "Voo não encontrado."

        Voos.nome = novo_nome
        if self.__dao.atualizar(Voos):
            return True, "Dados do voo alterados com sucesso!"
        return False, "Erro ao alterar os dados do voo."

    def deletar_Voo(self, cod):
        Voo = self.__dao.buscar_por_cpf(cod)
        if not Voo:
            return False, "Voo não encontrado."

        if self.__dao.deletar(cod):
            return True, "Voo deletado com sucesso!"
        return False, "Erro ao deletar o voo."

