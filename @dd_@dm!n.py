import os
import pymongo
import bcrypt
from validate_docbr import CPF
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGO_URI')
client = pymongo.MongoClient(uri)

db = client["lagol_airlines"]
collection = db["admins"]

def adicionar_registro(nome, cpf, senha):
    # Validação do CPF
    cpf_objeto = CPF()
    if not cpf_objeto.validate(cpf):
        raise ValueError("CPF inválido")

    hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    collection.insert_one({"username": nome, "senha": hashed_password, "cpf": cpf})

admin_nome = str(input("Digite o nome do Admin: "))
admin_cpf = str(input("Digite o CPF do Admin: "))

admin_senha = input("Digite a senha do Admin: ")

adicionar_registro(admin_nome, admin_cpf, admin_senha)
