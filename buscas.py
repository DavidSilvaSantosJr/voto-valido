import conexao_mongo 
import time
from funcoes import consultas_maps
from unidecode import unidecode
import re

def resumo_semana(cidade): #filtar os 10 com mais likes e comentarios, dos últimos 7 dias

    query_result =  list(conexao_mongo.uf_collection.find({
        'city_formated': cidade
    }
        ,
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
    if len(query_result) <1:
        return 'Ops!, parece que não há problemas registrados nessa cidade, verifique se tudo foi digitado corretamente, e tente novamente.'
    resposta_formatada = str(f"Esses são os problemas mais repercurtidos da cidade:\n\n\n") ###exibir ceerrtoo###

    #forma para exibir na mensagem
    for i in query_result:
        print(i['location'])
        if i['like'] == 0:
            resposta_formatada = f"\n{resposta_formatada} {i['descricao']}, no bairro {i['bairro']}, ainda com nenhum like; \n\n"
        if i['like'] >=1:
            resposta_formatada = f"\n{resposta_formatada} {i['descricao']}, no bairro {i['bairro']} com {i['like']} like(s); \n\n"


    resposta_formatada += str(f"\nVocê também pode ver os problemas em mapas, e entender melhor o que acontece na sua e em outras cidades futuramente em uma plataforma que estamos desenvolvendo!")


    return resposta_formatada
