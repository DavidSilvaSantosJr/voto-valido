import conexao_mongo 



def resumo_semana(uf, cidade): #filtar os 10 com mais likes e comentarios, dos últimos 7 dias
    uf = uf.upper()
    if uf == "SAO PAULO":
        query_result =  list(conexao_mongo.sao_paulo_collection.find({
            "cidade": cidade
            },
            {
                "uf":1,
                "descricao": 1
            }))
        print(query_result)   

    resposta_formatada = str(
        f"Em {cidade}, {uf.capitalize()}, esses são os problemas mais repercurtidos:\n"
    
    )
    resposta_descricao = []
    for i in query_result: 
        texto = i['descricao']
        resposta_descricao.append(i['descricao'])
        resposta_formatada = "\n"+resposta_formatada + texto +' com [total de llikes] likes, e [total de comentarios] comentários. ' + "\n\n"
        

    print(resposta_descricao)
    print('resposta fromatada e concatendada:\n\n\n\n', resposta_formatada)
    return resposta_formatada
