import conexao_mongo 

def resumo_semana(uf, cidade):
    uf = uf.upper()
    if uf == "SP" or "SAO PAULO":
        query_result =  list(conexao_mongo.sao_paulo_collection.find({
            "cidade": cidade
            },
            {
                "uf":1,
                "descricao": 1
            }))
        
    resposta_descricao = []
    for i in query_result: 
        resposta_descricao.append(i['descricao'])
    print(resposta_descricao)
    return resposta_descricao
