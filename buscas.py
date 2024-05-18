import conexao_mongo 
import time
from funcoes import consultas_maps

def resumo_semana(uf, cidade): #filtar os 10 com mais likes e comentarios, dos últimos 7 dias
    uf = uf.upper()
    if uf == "SAO PAULO":
        query_result =  list(conexao_mongo.sao_paulo_collection.find({
            "city": cidade
            },
            {   "_id":0,
                "location":1,
                "uf":1,
                "descricao": 1,
                "like": 1,
                "bairro":1

            }).sort({
                'like': -1
            }).limit(10)
            )
        
        print(query_result)
        resposta_formatada = str(f"Em {cidade}, {uf.capitalize()}, esses são os problemas mais repercurtidos:\n")
    
    #forma para exibir na mensagem
    for i in query_result:
        print(i['location'])
        resposta_formatada = f"\n{resposta_formatada} {i['descricao']}, no bairro {i['bairro']} com {i['like']} like(s); \n\n"

    resposta_formatada += str(f"\nVocê pode ver os problemas em mapas, e entender melhor o que acontece em {cidade}, na nossa plataforma -> [LINK PLATAFORMA]!")
    
    
    return resposta_formatada
