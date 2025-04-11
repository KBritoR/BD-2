from pymongo import MongoClient

class Database:
    def __init__(self, connection_string="mongodb://localhost:27017/", database_name="motoristas_db"):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db["motoristas"]