from dao.DAOVoo import DAOVoo
from model.Voos import Voos
from model.Aeronaves import Aeronaves
from model.Pessoas.Pilotos import Pilotos
from model.Pessoas.Aeromocas import Aeromocas
from datetime import datetime

class ControladorVoo:
    def __init__(self):
        self.dao_voos = DAOVoo()

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
                raise ValueError("Entrada em 'aeronave' inválida, tente novamente")

            # Validação da Origem
            if len(origem) < 3:
                raise ValueError("Entrada em 'origem' inválida, tente novamente")

            # Validação do Destino
            if len(destino) < 3 or destino == origem:
                raise ValueError("Entrada em 'destino' inválida, tente novamente")

            # Validação da Data
            data_obj = datetime.strptime(data, '%d/%m/%Y')
            if data_obj <= datetime.now():
                raise ValueError("Entrada em 'data' inválida, tente novamente")

            # Validação do Piloto
            if not piloto:
                raise ValueError("Entrada em 'piloto' inválida, tente novamente")

            # Validação do Copiloto
            if not copiloto:
                raise ValueError("Entrada em 'copiloto' inválida, tente novamente")

            # Validação da Aeromoça 1
            if not aeromoca1:
                raise ValueError("Entrada em 'aeromoça 1' inválida, tente novamente")

            # Validação da Aeromoça 2
            if not aeromoca2:
                raise ValueError("Entrada em 'aeromoça 2' inválida, tente novamente")

            # Validação da Hora de Decolagem
            hora_obj = datetime.strptime(hora, '%H:%M').time()
           
            if hora_obj.hour >= 24 or hora_obj.minute >= 60:
                raise ValueError("Entrada em 'hora de decolagem' inválida, tente novamente")

            # Gerar código único
            codigo_voo = self.gerar_codigo_voo()

            # Criar o voo
            voo = Voos(
                cod=codigo_voo,
                aeronave=aeronave,
                assentos={},  # Implementar lógica para definir assentos
                origem=origem,
                destino=destino,
                data=data_obj,  # Usando data_obj após a validação
                horario_decolagem=hora_obj,  # Usando hora_obj após a validação
                piloto=piloto,
                copiloto=copiloto,
                aeromoca1=aeromoca1,
                aeromoca2=aeromoca2
            )

            # Persistir voo
            if self.dao_voos.adicionar(voo):
                return True, "Cadastro de voo realizado com sucesso"
            else:
                return False, "Erro ao cadastrar o voo."

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
            return self.dao_voos.buscar_por_codigo(cod)
        except Exception as e:
            print(f"Erro ao buscar voo: {e}")
            return None

    def alterar_voo(self, cod, aeronave, origem, destino, data, hora, piloto, copiloto, aeromoca1, aeromoca2):
        #RETIRAR ESSA BUSCA POR VOO
        voo = self.buscar_voo_por_codigo(cod)
        if not voo:
            return False, "Voo não encontrado."
        print(voo)
        # Atualizar informações do voo com verificações de parâmetros
        try:
            if aeronave:
                voo.aeronave = aeronave
            print("A1")
            if origem:
                voo.origem = origem
            print("A2")
            if destino:
                voo.destino = destino
            print("A3")
            if data:
                voo.data = data
            print("A4")
            if hora:
                hora_obj = datetime.strptime(hora, '%H:%M').time()
                voo.horario_decolagem = hora_obj
                print(hora_obj)
                print(hora_obj.hour)
            print("A5")
            if piloto:
                voo.piloto =piloto
            print("A6")
            if copiloto:    
                voo.copiloto = copiloto
            print("A7")
            if aeromoca1:            
                voo.aeromoca1 = aeromoca1
            print("A8")
            if aeromoca2:
                voo.aeromoca2 = aeromoca2

            print("INDo pro atualizar")

            if self.dao_voos.atualizar(voo):
                return True, "Dados do voo alterados com sucesso!"
        except Exception as e:
            print(f"Erro ao atualizar voo no controlador: {e}")
            return False, "Erro ao alterar os dados do voo."

    def deletar_voo(self, cod):
        voo = self.buscar_voo_por_codigo(cod)
        if not voo:
            print("Voo não encontrado.")
            return False, "Voo não encontrado."

        try:
            if self.dao_voos.deletar(cod):
                return True, "Voo deletado com sucesso!"
        except Exception as e:
            print(f"Erro ao deletar voo: {e}")
        return False, "Erro ao deletar o voo."
