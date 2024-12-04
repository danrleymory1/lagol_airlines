from datetime import datetime
from model.Reservas import Reservas
from dao.DAOReserva import DAOReserva
from dao.DAOVoo import DAOVoo
from dao.DAOAeronaves import DAOAeronaves
import random
import string

class ControladorReserva:
    def __init__(self):
        self.__dao_reserva = DAOReserva()
        self.__dao_voo = DAOVoo()
        self.__dao_aeronave = DAOAeronaves()

    def cadastrar_reserva(self, passageiro, cliente, voo_cod):
        print(cliente)
        print(cliente.cpf)

        # Gerar um código único para a reserva
        while True:
            cod = ''.join(random.choices(string.digits + string.ascii_uppercase, k=5))
            if self.validar_codigo(cod):
                break

        # Buscar o voo pelo código
        voo = self.__dao_voo.buscar_por_codigo(voo_cod)
        if not voo:
            return False, "Voo não encontrado."

        # Coletar todos os assentos disponíveis (com valor `None`)
        assentos_livres = [
            chave for assento in voo.assentos
            for chave, valor in assento.items()
            if valor is None
        ]

        if not assentos_livres:
            return False, "Não há assentos disponíveis para este voo."

        # Selecionar um assento aleatório entre os disponíveis
        assento_livre = random.choice(assentos_livres)

        # Atualizar o assento selecionado no voo
        for assento in voo.assentos:
            if assento_livre in assento:
                assento[assento_livre] = cod
                break

        # Persistir a atualização do voo no banco de dados
        if not self.__dao_voo.atualizar(voo):
            return False, "Erro ao atualizar informações do voo no banco de dados."

        # Criar a reserva com o assento selecionado
        reserva = Reservas(cod=cod, passageiro=passageiro, cliente=cliente, voo=voo_cod, assento=assento_livre)

        print(reserva)

        # Adicionar a reserva ao banco de dados
        if self.__dao_reserva.adicionar(reserva):
            return cod, "Reserva realizada com sucesso!"
        else:
            return False, "Erro ao cadastrar a reserva. Tente novamente."



    def validar_codigo(self, cod):
        if self.__dao_reserva.buscar_por_cod(cod):
            return False
        return True

    def buscar_reserva_por_cod(self, cod):
        return self.__dao_reserva.buscar_por_cod(cod)

    def buscar_reservas_por_cliente(self, cpf_cliente):
        return self.__dao_reserva.buscar_reservas({"cliente": cpf_cliente})

    def deletar_reserva(self, cod):
        reserva = self.__dao_reserva.buscar_por_cod(cod)
        if not reserva:
            return False, "Reserva não encontrada."

        sucesso = self.__dao_reserva.deletar(cod)
        if sucesso:
            self.liberar_assento(cod, reserva.assento)
            return True, "Reserva deletada com sucesso!"
        else:
            return False, "Erro ao deletar reserva. Tente novamente."
        
    def deletar_reservas_por_voo(self, voo_cod):
        print(f"Deletando reservas do voo {voo_cod}")
        reservas = self.__dao_reserva.buscar_reservas({"voo": int(voo_cod)})
        print(f"Reservas encontradas: {reservas}")
        for reserva in reservas:
            self.deletar_reserva(reserva.cod)

    def selecionar_assento_disponivel(self, aeronave, voo):
        total_assentos = [f"{row}{chr(65 + col)}" for row in range(1, aeronave.fileiras + 1) for col in range(aeronave.assentos_por_fileira)]
        ocupados = list(voo.assentos.values()) if isinstance(voo.assentos, dict) else []
        disponiveis = [assento for assento in total_assentos if assento not in ocupados]
        return disponiveis[0] if disponiveis else None

    def listar_fileiras_disponiveis(self, voo_cod):
        """Retorna uma lista de fileiras disponíveis com base no código do voo."""
        voo = self.__dao_voo.buscar_por_codigo(voo_cod)
        if not voo or not voo.assentos:
            return []

        # Extrair fileiras únicas com base nos assentos do voo
        fileiras = set(assento[:-1] for assento_map in voo.assentos for assento in assento_map.keys())
        return sorted(fileiras)

    def listar_assentos_disponiveis(self, voo_cod, fileira):
        voo = self.__dao_voo.buscar_por_codigo(voo_cod)
        if not voo or not voo.assentos:
            return []

        # Filtrar assentos da fileira especificada
        total_assentos = [assento for assento_map in voo.assentos for assento in assento_map.keys() if
                          assento.startswith(fileira)]
        ocupados = [assento for assento_map in voo.assentos for assento, reserva in assento_map.items() if
                    reserva is not None]

        return [assento for assento in total_assentos if assento not in ocupados]

    def liberar_assento(self, reserva_cod, assento):

        reserva = self.__dao_reserva.buscar_por_cod(reserva_cod)
        if not reserva:
            return False, "Reserva não encontrada."

        voo = self.__dao_voo.buscar_por_codigo(reserva.voo)
        if not voo:
            return False, "Voo não encontrado."

        if assento not in voo.assentos:
            return False, "Assento não ocupado."
        else:
            del voo.assentos[assento]
            sucesso = self.__dao_voo.atualizar(voo)
            if sucesso:
                reserva.assento = None
                self.__dao_reserva.atualizar(reserva)
                return True, "Assento liberado com sucesso."
            else:
                return False, "Erro ao liberar o assento."

    def atualizar_assento(self, reserva_cod, novo_assento):
        reserva = self.__dao_reserva.buscar_por_cod(reserva_cod)
        if not reserva:
            return False, "Reserva não encontrada."

        voo = self.__dao_voo.buscar_por_codigo(reserva.voo)
        if not voo:
            return False, "Voo não encontrado."

        # Verificar se o assento já está ocupado
        ocupados = [assento for assento_map in voo.assentos for assento, cod_reserva in assento_map.items() if
                    cod_reserva is not None]
        if novo_assento in ocupados:
            return False, "Assento já ocupado."

        # Atualizar a lista de assentos no voo
        for assento_map in voo.assentos:
            if novo_assento in assento_map:
                assento_map[novo_assento] = reserva.cod
                break

        sucesso = self.__dao_voo.atualizar(voo)
        if sucesso:
            reserva.assento = novo_assento
            self.__dao_reserva.atualizar(reserva)
            return True, "Assento atualizado com sucesso."
        else:
            return False, "Erro ao atualizar o assento."

    def validar_data(self, data):
        try:
            data = datetime.strptime(data, "%d/%m/%Y")
                        
            hoje = datetime.now().date()
                        
            if data.date() > hoje:
                return False, "Data de nascimento inválida."
            
            return True, "Data válida."
        except ValueError:
            return False, "Data de nascimento inválida."
        
    def validar_nome(self, nome):

        if not nome:
            return False, "Nome inválido."
        elif len(nome) < 3:
            return False, "Nome inválido."
        return True, "Nome válido."
    
    def validar_cpf(self, cpf):
        if not cpf:
            return False, "CPF inválido."
        elif len(cpf) != 11:
            return False, "CPF inválido."
        elif not cpf.isdigit():
            return False, "CPF inválido."
        return True, "CPF válido."

