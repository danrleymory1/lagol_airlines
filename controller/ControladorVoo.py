from dao.DAOVoo import DAOVoo
from model.Voos import Voos
from dao.DAOAeronaves import DAOAeronaves
from model.Aeronaves import Aeronaves
from model.Pessoas.Pilotos import Pilotos
from model.Pessoas.Aeromocas import Aeromocas
from datetime import datetime

class ControladorVoo:
    def __init__(self, controlador):
        self.dao_voos = DAOVoo()
        self.__controlador = controlador
        self.dao_aeronave = DAOAeronaves()

    def gerar_codigo_voo(self):
        # Gera um código de voo automaticamente, incrementando a partir do último código.
        voos = self.dao_voos.buscar_voos()
        if voos:
            return max([voo.cod for voo in voos]) + 1  # Incrementa o código do voo
        else:
            return 1  # Caso não haja voos registrados, começa do código 1

    def cadastrar_voo(self, aeronave, origem, destino, data, hora, piloto, copiloto, aeromoca1, aeromoca2):
        try:
            # Validação da Aeronave
            if not aeronave:
                raise ValueError("Entrada em 'Avião' inválida, tente novamente")

            # Validação da Origem
            if len(origem) < 3:
                raise ValueError("Entrada em 'origem' inválida, tente novamente")

            # Validação do Destino
            if len(destino) < 3 or destino == origem:
                raise ValueError("Entrada em 'destino' inválida, tente novamente")

            # Validação da Data
            if not data:  # Verifica se o campo de data está vazio
                raise ValueError("Entrada em 'data' inválida, tente novamente")
            data = datetime.strptime(data, '%d/%m/%Y')
            if data <= datetime.now():
                raise ValueError("Entrada em 'data' inválida, tente novamente")

            # Validação do Piloto
            if not piloto:
                raise ValueError("Entrada em 'piloto' inválida, tente novamente")

            # Validação do Copiloto
            if not copiloto:
                raise ValueError("Entrada em 'copiloto' inválida, tente novamente")
            if piloto == copiloto:  # Verifica se piloto e copiloto são os mesmos
                raise ValueError("Entrada em 'copiloto' inválida, tente novamente")

            # Validação da Aeromoça 1
            if not aeromoca1:
                raise ValueError("Entrada em 'aeromoça 1' inválida, tente novamente")

            # Validação da Aeromoça 2
            if not aeromoca2:
                raise ValueError("Entrada em 'aeromoça 2' inválida, tente novamente")
            if aeromoca1 == aeromoca2:  # Verifica se as aeromoças são as mesmas
                raise ValueError("Entrada em 'aeromoça 2' inválida, tente novamente")

            # Validação da Hora de Decolagem
            try:
                datetime.strptime(hora, '%H:%M').time()
            except ValueError:
                return False, "Entrada em 'hora de decolagem' inválida, tente novamente"


            codigo_voo = self.gerar_codigo_voo()
            aeronave_obj = self.dao_aeronave.buscar_por_modelo(aeronave)
            if not aeronave_obj:
                raise ValueError("Entrada em 'Avião' inválida, tente novamente")
            
            assentos = []
            for fileira in range(1, aeronave_obj.fileiras + 1):
                for coluna in range(aeronave_obj.assentos_por_fileira):
                    assento = f"{fileira}{chr(65 + coluna)}"
                    assentos.append({assento: None})
            
            voo = Voos(cod=codigo_voo, aeronave=aeronave_obj, assentos=assentos, origem=origem, destino=destino,
                       data=data, horario_decolagem=hora, piloto=piloto, copiloto=copiloto, aeromoca1=aeromoca1,
                       aeromoca2=aeromoca2)

            if self.dao_voos.adicionar(voo):
                return True, "Cadastro de voo realizado com sucesso"
            return False, "Erro ao cadastrar voo."
        except ValueError as e:
            return False, str(e)

    def buscar_todos_voos(self):
        try:
            return self.dao_voos.buscar_voos()
        except Exception as e:
            print(f"Erro ao buscar todos os voos: {e}")
            return []

    def buscar_voo_por_codigo(self, cod):
        try:
            voo_dict = self.dao_voos.buscar_por_codigo(cod)
            if voo_dict:
                return self.dao_voos.dict_to_voo(voo_dict)
            return None
        except Exception as e:
            print(f"Erro ao buscar voo: {e}")
            return None

    def alterar_voo(self, voo, aeronave=None, origem=None, destino=None, data=None, hora=None, piloto=None,
                    copiloto=None, aeromoca1=None, aeromoca2=None):
        try:
            if not aeronave:
                raise ValueError("Entrada em 'Avião' inválida, tente novamente")

            # Validação da Origem
            if len(origem) < 3:
                raise ValueError("Entrada em 'origem' inválida, tente novamente")

            # Validação do Destino
            if len(destino) < 3 or destino == origem:
                raise ValueError("Entrada em 'destino' inválida, tente novamente")

            # Validação da Data
            if not data:  # Verifica se o campo de data está vazio
                raise ValueError("Entrada em 'data' inválida, tente novamente")
            data = datetime.strptime(data, '%d/%m/%Y')
            if data <= datetime.now():
                raise ValueError("Entrada em 'data' inválida, tente novamente")

            # Validação do Piloto
            if not piloto:
                raise ValueError("Entrada em 'piloto' inválida, tente novamente")

            # Validação do Copiloto
            if not copiloto:
                raise ValueError("Entrada em 'copiloto' inválida, tente novamente")
            if piloto == copiloto:  # Verifica se piloto e copiloto são os mesmos
                raise ValueError("Entrada em 'copiloto' inválida, tente novamente")

            # Validação da Aeromoça 1
            if not aeromoca1:
                raise ValueError("Entrada em 'aeromoça 1' inválida, tente novamente")

            # Validação da Aeromoça 2
            if not aeromoca2:
                raise ValueError("Entrada em 'aeromoça 2' inválida, tente novamente")
            if aeromoca1 == aeromoca2:  # Verifica se as aeromoças são as mesmas
                raise ValueError("Entrada em 'aeromoça 2' inválida, tente novamente")

            # Validação da Hora de Decolagem
            try:
                datetime.strptime(hora, '%H:%M').time()
            except ValueError:
                return False, "Entrada em 'hora de decolagem' inválida, tente novamente"


            # Busca a aeronave se necessário
            if aeronave:
                aeronave_obj = self.dao_aeronave.buscar_por_modelo(aeronave)
                if not aeronave_obj:
                    raise ValueError("Entrada em 'Avião' inválida, tente novamente")
                voo.aeronave = aeronave_obj  # Atualiza com o objeto aeronave correto

            # Atualiza os campos do voo
            if origem:
                voo.origem = origem
            if destino:
                voo.destino = destino
            if data:
                voo.data = data
            if hora:
                voo.horario_decolagem = hora
            if piloto:
                voo.piloto = piloto
            if copiloto:
                voo.copiloto = copiloto
            if aeromoca1:
                voo.aeromoca1 = aeromoca1
            if aeromoca2:
                voo.aeromoca2 = aeromoca2

            # Persistir no DAO
            sucesso = self.dao_voos.atualizar(voo)
            if sucesso:
                return True, "Informação do voo alterado com sucesso!"
            else:
                return False, "Erro ao alterar voo."
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            print(f"Erro inesperado ao alterar voo: {e}")
            return False, "Erro inesperado ao alterar voo."

    def deletar_voo(self, cod):
        voo = self.buscar_voo_por_codigo(cod)
        if not voo:
            return False, "Voo não encontrado."

        try:
            if self.dao_voos.deletar(cod):
                self.__controlador.controlador_reserva.deletar_reservas_por_voo(cod)
                return True, "Voo exclúido com sucesso!"
        except Exception as e:
            print(f"Erro ao deletar voo: {e}")
        return False, "Erro ao deletar o voo."
