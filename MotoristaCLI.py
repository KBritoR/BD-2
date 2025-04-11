from SimpleCLI import SimpleCLI
from MotoristaDAO import MotoristaDAO
from Corrida import Corrida
from Passageiro import Passageiro

class MotoristaCLI(SimpleCLI):
    def __init__(self, motorista_dao: MotoristaDAO):
        super().__init__()
        self.motorista_dao = motorista_dao
        self.add_command("create", self.create_motorista)
        self.add_command("read", self.read_motorista)
        self.add_command("update", self.update_motorista)
        self.add_command("delete", self.delete_motorista)

    def create_passageiro(self):
        nome = input("Enter the nome do passageiro: ")
        documento = input("Enter the documento do passageiro: ")
        return Passageiro(nome, documento)

    def create_corrida(self):
        nota = int(input("Enter the nota da corrida (0-5): "))
        distancia = float(input("Enter the distancia da corrida (km): "))
        valor = float(input("Enter the valor da corrida: "))
        print("\nInformações do Passageiro:")
        passageiro = self.create_passageiro()
        return Corrida(nota, distancia, valor, passageiro)

    def create_motorista(self):
        corridas = []
        while True:
            print("\nAdicionando nova corrida:")
            corridas.append(self.create_corrida())
            continuar = input("Deseja adicionar outra corrida? (s/n): ")
            if continuar.lower() != 's':
                break
        
        nota = int(input("\nEnter the nota do motorista (0-5): "))
        self.motorista_dao.create_motorista(corridas, nota)

    def read_motorista(self):
        id = input("Enter the id: ")
        motorista = self.motorista_dao.read_motorista_by_id(id)
        if motorista:
            print(f"\nMotorista ID: {motorista['_id']}")
            print(f"Nota: {motorista['nota']}")
            print("Corridas:")
            for i, corrida in enumerate(motorista['corridas'], 1):
                print(f"\n  Corrida {i}:")
                print(f"  Nota: {corrida['nota']}")
                print(f"  Distancia: {corrida['distancia']} km")
                print(f"  Valor: R${corrida['valor']:.2f}")
                print("  Passageiro:")
                print(f"    Nome: {corrida['passageiro']['nome']}")
                print(f"    Documento: {corrida['passageiro']['documento']}")

    def update_motorista(self):
        id = input("Enter the id do motorista a ser atualizado: ")
        print("\nAtualize as corridas:")
        corridas = []
        while True:
            print("\nAdicionando nova corrida:")
            corridas.append(self.create_corrida())
            continuar = input("Deseja adicionar outra corrida? (s/n): ")
            if continuar.lower() != 's':
                break
        
        nota = int(input("\nEnter the nova nota do motorista (0-5): "))
        self.motorista_dao.update_motorista(id, corridas, nota)

    def delete_motorista(self):
        id = input("Enter the id do motorista a ser deletado: ")
        self.motorista_dao.delete_motorista(id)
        
    def run(self):
        print("\nWelcome to the Motorista CLI!")
        print("Available commands: create, read, update, delete, quit")
        super().run()