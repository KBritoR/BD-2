from pymongo import MongoClient
from bson.objectid import ObjectId

class Database:
    def __init__(self, connection_string="mongodb://localhost:27017/", database_name="motoristas_db"):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db["motoristas"]

class Passageiro:
    def __init__(self, nome: str, documento: str):
        self.nome = nome
        self.documento = documento

    def to_dict(self):
        return {
            "nome": self.nome,
            "documento": self.documento
        }

class Corrida:
    def __init__(self, nota: int, distancia: float, valor: float, passageiro: Passageiro):
        self.nota = nota
        self.distancia = distancia
        self.valor = valor
        self.passageiro = passageiro

    def to_dict(self):
        return {
            "nota": self.nota,
            "distancia": self.distancia,
            "valor": self.valor,
            "passageiro": self.passageiro.to_dict()
        }

class MotoristaDAO:
    def __init__(self, database):
        self.db = database

    def create_motorista(self, corridas: list, nota: int):
        try:
            corridas_dict = [corrida.to_dict() for corrida in corridas]
            res = self.db.collection.insert_one({
                "corridas": corridas_dict,
                "nota": nota
            })
            print(f"Motorista created with id: {res.inserted_id}")
            return res.inserted_id
        except Exception as e:
            print(f"An error occurred while creating motorista: {e}")
            return None

    def read_motorista_by_id(self, id: str):
        try:
            res = self.db.collection.find_one({"_id": ObjectId(id)})
            print(f"Motorista found: {res}")
            return res
        except Exception as e:
            print(f"An error occurred while reading motorista: {e}")
            return None

    def update_motorista(self, id: str, corridas: list, nota: int):
        try:
            corridas_dict = [corrida.to_dict() for corrida in corridas]
            res = self.db.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {
                    "corridas": corridas_dict,
                    "nota": nota
                }}
            )
            print(f"Motorista updated: {res.modified_count} document(s) modified")
            return res.modified_count
        except Exception as e:
            print(f"An error occurred while updating motorista: {e}")
            return None

    def delete_motorista(self, id: str):
        try:
            res = self.db.collection.delete_one({"_id": ObjectId(id)})
            print(f"Motorista deleted: {res.deleted_count} document(s) deleted")
            return res.deleted_count
        except Exception as e:
            print(f"An error occurred while deleting motorista: {e}")
            return None

class SimpleCLI:
    def __init__(self):
        self.commands = {}

    def add_command(self, name, function):
        self.commands[name] = function

    def run(self):
        while True:
            command = input("Enter a command: ")
            if command == "quit":
                print("Goodbye!")
                break
            elif command in self.commands:
                self.commands[command]()
            else:
                print("Invalid command. Try again.")

class MotoristaCLI(SimpleCLI):
    def __init__(self, motorista_dao):
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

# Main execution
if __name__ == "__main__":
    db = Database()
    motorista_dao = MotoristaDAO(db)
    cli = MotoristaCLI(motorista_dao)
    cli.run()