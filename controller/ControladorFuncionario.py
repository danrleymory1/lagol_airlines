from dns.name import empty
from model.Pessoas.Pilotos import Pilotos
from model.Pessoas.Aeromocas import Aeromocas
from dao.DAOFuncionario import DAOFuncionario
from validate_docbr import CPF

class ControladorFuncionario:
    def __init__(self):
        self.__dao = DAOFuncionario()

    def cadastrar_funcionario(self, nome, cpf, cargo):
        if not nome:
            return False, "Adicione um nome ao funcionário."

        cpf_objeto = CPF()
        if not cpf_objeto.validate(cpf):
            raise ValueError("CPF Inválido")
        if self.__dao.buscar_por_cpf(cpf):
            return False, "Funcionário com esse CPF já cadastrado."

        if cargo == "Piloto":
            funcionario = Pilotos(nome=nome, cpf=cpf)
        elif cargo == "Aeromoca":
            funcionario = Aeromocas(nome=nome, cpf=cpf)
        else:
            return False, "Cargo inválido."

        if self.__dao.adicionar(funcionario):
            return True, "Cadastro realizado com sucesso!"
        else:
            return False, "Erro ao cadastrar funcionário. Tente novamente."

    def buscar_todos_funcionarios(self):
        return self.__dao.buscar_todos()

    def buscar_funcionario_por_cpf(self, cpf):
        return self.__dao.buscar_por_cpf(cpf)

    def alterar_funcionario(self, cpf, novo_nome):
        funcionario = self.__dao.buscar_por_cpf(cpf)
        if not funcionario:
            return False, "Funcionário não encontrado."

        funcionario.nome = novo_nome
        if self.__dao.atualizar(funcionario):
            return True, "Nome do funcionário alterado com sucesso!"
        return False, "Erro ao alterar o nome do funcionário."

    def deletar_funcionario(self, cpf):
        funcionario = self.__dao.buscar_por_cpf(cpf)
        if not funcionario:
            return False, "Funcionário não encontrado."

        if self.__dao.deletar(cpf):
            return True, "Funcionário deletado com sucesso!"
        return False, "Erro ao deletar o funcionário."

