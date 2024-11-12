
from controller.ControladorReserva import ControladorReserva
from controller.ControladorCliente import Controladorcliente
from controller.ControladorAdminLogin import ControladorAdminLogin
from controller.ControladorFuncionario import ControladorFuncionario
from controller.ControladorVoo import ControladorVoo
from view.ViewLogin import TelaLogin

class ControladorSistema:
    def __init__(self):
        self.__controlador_cliente = Controladorcliente()
        self.__controlador_admin_login = ControladorAdminLogin()
        self.__controlador_funcionario = ControladorFuncionario()
        self.__controlador_voo = ControladorVoo()
        self.__controlador_reserva = ControladorReserva()

    @property
    def controlador_cliente(self):
        return self.__controlador_cliente

    @property
    def controlador_admin_login(self):
        return self.__controlador_admin_login

    @property
    def controlador_funcionario(self):
        return self.__controlador_funcionario

    @property
    def controlador_voo(self):
        return self.__controlador_voo
    
    @property
    def controlador_reserva(self):
        return self.__controlador_reserva

    def iniciar(self):
        app = TelaLogin(self)
        app.abrir()
