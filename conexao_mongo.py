import pymongo
from keys import STRING_CONNECTION


# Conectar ao servidor MongoDB (por padrão, o MongoDB roda em localhost, porta 27017)
client = pymongo.MongoClient(STRING_CONNECTION)

# banco de dados
unioes_federativas = client["unioes_federativas"]
# coleções
sao_paulo_collection = unioes_federativas["sao_paulo"]
parana_collection = unioes_federativas['parana']
rio_grande_do_sul_collection = unioes_federativas['rio_grande_do_sul']
santa_catarina_collection = unioes_federativas['santa_catarina']


def adicionar_dados(x, uf):
    if uf.upper() == 'SP':
        sao_paulo_collection.insert_one(x)
    if uf.upper() == 'PR':
        sao_paulo_collection.insert_one(x)    
    if uf.upper() == 'RS':
        sao_paulo_collection.insert_one(x)
    if uf.upper() == 'SC':
        sao_paulo_collection.insert_one(x)
