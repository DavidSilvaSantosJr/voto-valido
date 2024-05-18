import conexao_mongo 
import time

def resumo_semana(uf, cidade): #filtar os 10 com mais likes e comentarios, dos últimos 7 dias
    uf = uf.upper()
    if uf == "SAO PAULO":
        ultimos_5_dias = int() 
        query_result =  list(conexao_mongo.sao_paulo_collection.find({
            "city": cidade
            },
            {
                "uf":1,
                "descricao": 1,
                "like": 1

            }).sort({
                'like': -1
            }).limit(10)
            )
        
        print(query_result)   
    resposta_formatada = str(
        f"Em {cidade}, {uf.capitalize()}, esses são os problemas mais repercurtidos:\n"
    
    )
    #forma para exibir na mensagem
    resposta_descricao = []
    for i in query_result:
        resposta_descricao.append(i['descricao'])
        if i['like'] == 0:
            resposta_formatada = f"\n{resposta_formatada} {i['descricao']},no bairro [nome do bairro], ainda sem likes; \n\n"
        if i['like'] == 1:
            resposta_formatada = f"\n{resposta_formatada} {i['descricao']},no bairro [nome do bairro] com {i['like']} like; \n\n"
        if i['like'] >=2:
            resposta_formatada = f"\n{resposta_formatada} {i['descricao']},no bairro [nome do bairro] com {i['like']} likes; \n\n"

    resposta_formatada += str(f"\nVocê pode ver os problemas em mapas, e entender melhor o que acontece em {cidade}, na nossa plataforma -> [LINK PLATAFORMA]!")
    
    print(resposta_descricao)
    return resposta_formatada
