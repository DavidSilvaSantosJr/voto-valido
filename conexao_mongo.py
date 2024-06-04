import pymongo
from keys import STRING_CONNECTION


# Conectar ao servidor MongoDB (por padrão, o MongoDB roda em localhost, porta 27017)
client = pymongo.MongoClient(STRING_CONNECTION)

# banco de dados
unioes_federativas = client["unioes_federativas"]
# coleções
uf_collection = unioes_federativas["uf"]

def adicionar_dados(x): 
    uf_collection.insert_one(x)


def atualizar(chat_id, update):
    uf_collection.update_one(
        {"chat_id": chat_id}, #filtro
        {"$set": update}   #novas informaçoes
    )
