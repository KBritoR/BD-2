from bson.objectid import ObjectId
from Database import Database

class MotoristaDAO:
    def __init__(self, database: Database):
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