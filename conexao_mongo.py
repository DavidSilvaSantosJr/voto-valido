import pymongo
import telebot
from keys import STRING_CONNECTION

# Conectar ao servidor MongoDB (por padrão, o MongoDB roda em localhost, porta 27017)
client = pymongo.MongoClient(STRING_CONNECTION)

# banco de dados
unioes_federativas = client["unioes_federativas"]
# coleções
uf_collection = unioes_federativas["uf"]
itens_incompleto_collection = unioes_federativas['itens_incompletos']

def adicionar_dados(x):
    uf_collection.insert_one(x)
    

def adicionar_dados_incompletos(x): 
    itens_incompleto_collection.insert_one(x)


def atualizar(ObjectId, documento):
    itens_incompleto_collection.update_one(
        {"_id": ObjectId},    #filtro
        {"$set": documento}   #novas informaçoes
    )
