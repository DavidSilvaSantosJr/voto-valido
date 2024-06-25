import conexao_mongo 
from problemas import estados

def buscar_atualizacoes(cidade): #filtar os 5 com mais likes e comentarios, dos últimos 7 dias
    query_result =  list(
        conexao_mongo.uf_collection.find(
            {
            'localizacao.city': cidade
            }
            ,
            {   "_id":0,
                "localizacao.bairro":1,
                "localizacao.uf":1,
                "localizacao.like": 1,
                "sub_categoria":1

            }).sort({
                'like': -1
            }).limit(5)
        )
    if len(query_result) <1:
        return 'Ops!, parece que não há problemas registrados nessa cidade, clique em /start e fique a vontade para ser o primeiro(a)!'
    resposta_formatada = str(f"Esses são os problemas mais repercurtidos da cidade:\n\n\n")

    #forma para exibir na mensagem
    for i in query_result:
        if i['localizacao']['like'] == 0:
            resposta_formatada = f"\n{resposta_formatada} {i['sub_categoria']}, no bairro {i['localizacao']['bairro']}, ainda com nenhum like; \n\n"
        if i['localizacao']['like'] >=1:
            resposta_formatada = f"\n{resposta_formatada} {i['sub_categoria']}, no bairro {i['localizacao']['bairro']} com {i['localizacao']['like']} like(s); \n\n"

    resposta_formatada += str(f"\nVocê também pode ver os problemas em mapas, e entender melhor o que acontece na sua e em outras cidades futuramente em uma plataforma que estamos desenvolvendo!")
    
    return resposta_formatada

def busca_local(uf=False, cidade=False, uf_to_agr=None):
    # Agrupe por 'localizacao.uf' e retorne apenas 'city' distinto
    if uf:
        pipeline = [
        {
            "$group":{
                "_id": 0,
                "uf": {
                    "$addToSet":"$localizacao.uf"
                }
            }
        },
        {
            "$project":{
                "_id":0,
                "uf":1
                
            }
        }
        ] 
        resultado = list(conexao_mongo.uf_collection.aggregate(pipeline))
        print(resultado[0])
        return resultado[0]

    if cidade:
        pipeline = [{
            "$match":{
                "localizacao.uf":uf_to_agr
            }
        },
        {
            "$group":{
                "_id": 0,
                "cidades":{
                    "$addToSet":"$localizacao.city"
                }
            }
        },
        {
            "$project":{
                "_id":0,
                "cidades":1
            }
        }]

        resultado = list(conexao_mongo.uf_collection.aggregate(pipeline))
        print(resultado[0])
        return resultado[0]