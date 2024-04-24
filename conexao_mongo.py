import pymongo
import k


# Conectar ao servidor MongoDB (por padrão, o MongoDB roda em localhost, porta 27017)
client = pymongo.MongoClient(k.STRING_CONNECTION)

# banco de dados insert
unioes_federativas = client["unioes_federativas"]
sao_paulo_collection = unioes_federativas["sao paulo"]

#banco de dados para consulta
dtb = client["dtb"]
dtb_completo = dtb["dtb_completo"]



def adicionar_dados(x, uf):
    if uf == 'Sao Paulo':
        sao_paulo_collection.insert_one(x)
