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

    #Mudança
    def cadastrar_reserva(self, passageiro, cliente, voo_cod):
        while True:
            cod = ''.join(random.choices(string.digits + string.ascii_uppercase, k=5))
            if self.validar_codigo(cod):
                break

        # Buscar o voo e validar existência
        voo = self.__dao_voo.buscar_por_codigo(voo_cod)
        if not voo:
            return False, "Voo não encontrado."

        # Buscar todas as reservas do mesmo voo
        reservas_voo = self.__dao_reserva.buscar_reservas({"voo": voo_cod})

        # Determinar assentos disponíveis com base nas reservas
        assentos_ocupados = {r.assento for r in reservas_voo if r.assento is not None}
        assentos_disponiveis = [
            assento for assento_map in voo.assentos
            for assento, reserva_cod in assento_map.items()
            if assento not in assentos_ocupados
        ]

        if not assentos_disponiveis:
            return False, "Não há assentos disponíveis para este voo."

        # Selecionar um assento disponível aleatoriamente
        assento_livre = random.choice(assentos_disponiveis)

        # Atualizar o assento no banco de dados
        sucesso = self.__dao_voo.atualizar_assento(voo_cod, assento_livre, cod)
        if not sucesso:
            return False, "Erro ao atualizar informações do assento no banco de dados."

        # Criar e salvar a reserva
        reserva = Reservas(cod=cod, passageiro=passageiro, cliente=cliente, voo=voo_cod, assento=assento_livre)
        if self.__dao_reserva.adicionar(reserva):
            return cod, "Reserva realizada com sucesso!"
        else:
            self.__dao_voo.atualizar_assento(voo_cod, assento_livre, None)
            return False, "Erro ao cadastrar a reserva. Tente novamente."

    def validar_codigo(self, cod):
        if self.__dao_reserva.buscar_por_cod(cod):
            return False
        return True

    def buscar_reserva_por_cod(self, cod):
        return self.__dao_reserva.buscar_por_cod(cod)

    def buscar_reservas_por_voo(self, voo_cod):
        return self.__dao_reserva.buscar_reservas({"voo": voo_cod})

    def buscar_reservas_por_cliente(self, cpf_cliente):
        return self.__dao_reserva.buscar_reservas({"cliente": cpf_cliente})

    def deletar_reserva(self, cod):
        reserva = self.__dao_reserva.buscar_por_cod(cod)
        if not reserva:
            return False, "Reserva não encontrada."

        sucesso = self.__dao_reserva.deletar(cod)
        if sucesso:
            voo = self.__dao_voo.buscar_por_codigo(reserva.voo)
            if voo:
                self.__dao_voo.atualizar_assento(voo.cod, reserva.assento, None)
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
    #Mudança
    def listar_fileiras_disponiveis(self, voo_cod):
        voo = self.__dao_voo.buscar_por_codigo(voo_cod)
        if not voo or not voo.assentos:
            return []

        # Extrair todas as fileiras dos assentos ocupados
        fileiras = set()
        for assento_map in voo.assentos:
            for assento, reserva_cod in assento_map.items():
                if assento[:-1] not in fileiras:
                    fileiras.add(assento[:-1])

        return sorted(list(fileiras))
    #Mudança
    def listar_assentos(self, voo_cod, fileira):
        voo = self.__dao_voo.buscar_por_codigo(voo_cod)
        if not voo or not voo.assentos:
            return []

        # Garantir que os assentos do voo estão corretos
        print("Assentos no objeto voo (antes de processar):", voo.assentos)

        assentos_da_fileira = []
        for assento_map in voo.assentos:
            for assento, reserva_cod in assento_map.items():
                if assento.startswith(fileira):
                    estado = {
                        "assento": assento,
                        "ocupado": reserva_cod is not None  # Verificar se o assento está ocupado
                    }
                    assentos_da_fileira.append(estado)

        return sorted(assentos_da_fileira, key=lambda x: x["assento"])

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
    #Mudança
    def atualizar_assento(self, reserva_cod, novo_assento):
        # Buscar a reserva
        reserva = self.__dao_reserva.buscar_por_cod(reserva_cod)
        if not reserva:
            return False, "Reserva não encontrada."

        # Buscar todas as reservas do mesmo voo
        reservas_voo = self.__dao_reserva.buscar_reservas({"voo": reserva.voo})

        # Verificar se o novo assento já está ocupado
        for r in reservas_voo:
            if r.assento == novo_assento:
                return False, f"Assento {novo_assento} já está ocupado no voo {reserva.voo}."

        # Liberar o assento atual na reserva
        if reserva.assento:
            sucesso = self.__dao_voo.atualizar_assento(reserva.voo, reserva.assento, None)
            if not sucesso:
                return False, "Erro ao liberar o assento atual no banco de dados."

        # Ocupar o novo assento
        sucesso = self.__dao_voo.atualizar_assento(reserva.voo, novo_assento, reserva_cod)
        if not sucesso:
            return False, "Erro ao ocupar o novo assento no banco de dados."

        # Atualizar a reserva
        if self.__dao_reserva.atualizar_assento(reserva_cod, novo_assento):
            return True, "Assento atualizado com sucesso!"
        else:
            return False, "Erro ao atualizar o assento na reserva."

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

