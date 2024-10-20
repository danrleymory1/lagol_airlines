import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from abc import ABC, abstractmethod

load_dotenv()
uri = os.getenv('MONGO_URI')

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Conectado com muito sucesso!")
except Exception as e:
    print(e)

class DAO(ABC):
    def __init__(self):
        self.__client = MongoClient(uri)
        self.__db = self.__client['lagol_airlines']
        self.__counters = self.__db['counters']

    def get_next_cod(self, counter_name):
        counter = self.__counters.find_one_and_update(
            {"_id": counter_name},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True
        )
        return counter["seq"]

    @abstractmethod
    def adicionar(self, obj):
        pass

    @abstractmethod
    def buscar_por_cpf(self, cpf):
        pass

    def fechar_conexao(self):
        self.__client.close()

    @property
    def db(self):
        return self.__db