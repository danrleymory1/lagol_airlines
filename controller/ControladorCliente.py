from model.Pessoas.Clientes import Clientes
from dao.DAOCliente import DAOCliente
from validate_docbr import CPF
import bcrypt
from datetime import datetime


class Controladorcliente:
    def __init__(self):
        self.__dao = DAOCliente()
        self.cliente_logado = None

    def set_cliente_logado(self, cliente):
        self.cliente_logado = cliente

    
    def calcular_idade(self, data_nasc_str):
        data_nasc = datetime.strptime(data_nasc_str, "%d/%m/%Y")
        hoje = datetime.today()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        return idade

    def cadastrar_cliente(self, nome, cpf, data_nasc, senha, confirmar_senha):
        if not nome:
            return False, "Adicione um nome ao cliente."

        cpf_objeto = CPF()
        if not cpf_objeto.validate(cpf):
            return False, "CPF Inválido."

        if not data_nasc:
            return False, "Data de nascimento inválida."

        idade = self.calcular_idade(data_nasc)
        if idade < 18:
            return False, "Somente maiores de 18 anos podem se cadastrar."

        if not senha:
            return False, "Digite uma senha."

        if senha != confirmar_senha:
            return False, "As senhas não coincidem."

        if self.__dao.buscar_por_cpf(cpf):
            return False, "cliente com esse CPF já cadastrado."

        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        cliente = Clientes(nome=nome, cpf=cpf, data_nascimento=data_nasc, senha=hashed_senha)

        if self.__dao.adicionar(cliente):
            return True, "Cadastro realizado com sucesso!"
        else:
            return False, "Erro ao cadastrar cliente. Tente novamente."

    def validar_login(self, cpf, senha):
        cliente = self.__dao.buscar_por_cpf(cpf)
        if not cliente:
            return False, "cliente não encontrado."
        if bcrypt.checkpw(senha.encode('utf-8'), cliente.senha):
            self.set_cliente_logado(cliente)
            return True, "Login realizado com sucesso!"
        return False, "Senha incorreta."

    def alterar_dados_cliente(self, novo_nome=None, nova_data_nasc=None, nova_senha=None, confirmar_senha=None):
        if not self.cliente_logado:
            return False, "Nenhum cliente logado."

        if novo_nome:
            self.cliente_logado.nome = novo_nome

        if nova_data_nasc:
            idade = self.calcular_idade(nova_data_nasc)
            if idade < 18:
                return False, "Somente maiores de 18 anos podem alterar a data de nascimento para essa nova data."
            self.cliente_logado.data_nascimento = nova_data_nasc

        if nova_senha:
            if nova_senha != confirmar_senha:
                return False, "As senhas não coincidem."
            self.cliente_logado.senha = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())

        if self.__dao.atualizar(self.cliente_logado):
            return True, "Dados alterados com sucesso!"
        else:
            return False, "Erro ao alterar dados. Tente novamente."

    def deletar_cliente(self):
        if not self.cliente_logado:
            return False, "Nenhum cliente logado para deletar."

        sucesso = self.__dao.deletar(self.cliente_logado.cpf)
        if sucesso:
            self.cliente_logado = None
            return True, "cliente deletado com sucesso!"
        else:
            return False, "Erro ao deletar cliente. Tente novamente."
