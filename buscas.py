import pymongo
import conexao_mongo 



def resumo_semana(local_a_consultar):
    return list(conexao_mongo.colecao.find({"localizacao":local_a_consultar},
                                                 {
                                                      "local_de_envio": 0,
                                                      "imagem":0,
                                                      "_id":0
                                                  }
                                                  ))

def adicionar_dados(x, uf):
    if uf.upper() == "SÃO PAULO":
        conexao_mongo.colecao_uf_insert_sp(x)

def consultar_estado(x):
    try:
        consulta = conexao_mongo.dtb_completo.find_one({"Nome_UF": x})
        return consulta["Nome_UF"]
    except TypeError:
        text = f"Verifique se o nome do estado foi digitado corretamente, e tente mais suma vez.\n"
        f"Não encontrei nenhum estado chamado {x}!"
        return text

def consultar_cidade(x, uf):
    try:
        consulta = conexao_mongo.dtb_completo.find_one({"Nome_UF":uf, "Nome_Municipio":x})
        return consulta["Nome_Municipio"]
    except TypeError:
        text = f"Verifique se o nome do estado municipio foi digitado corretamente, e tente mais suma vez.\n"
        f"Não encontrei {x} em {uf}!"
        return text