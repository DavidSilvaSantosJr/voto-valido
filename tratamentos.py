import requests
import unidecode
import json
from keys import key
#import keys as keys
api_key = key

def texto_padrao(boas_vindas=None, agradecimento=None):
    if boas_vindas:
        texto = str(
            "Olá! sou o Veve, o bot que vai ajudar a cidade.\n\n"
            "Diga onde está o problema, envie uma foto e descreva o que está acontecendo ali.\n\n\n"
            "Ah, e mesmo que você esteja longe do local do problema, é possivel adiciona-lo na plataforma. Caso não tenha a imagem"
            "basta enviar o link para alguém que esteja por lá.\n\n\n"
            "Siga as instruções, e seja bem vindo!\n"
            "caso eu pare,dê algum erro, ou pare de dar respostas, \n\n\nclique abaixo, em recomeçar que o processo será refeito\n\n"
            "/recomeçar"

        )
        return texto
    
    elif agradecimento:
        texto = str(
            "Obrigado por ajudar a tornar nossa cidade um lugar melhor!\n\n"


            "Seu relato é extremamente importante para nós, pois nos ajuda a identificar áreas que precisam de melhorias e a tomar "
            "as medidas necessárias para resolver os problemas que afetam nossa comunidade"

            "Voce pode ver esse e outros problemas em [link plataforma], não esqueça de compartilhar esse problemas com outros moradores da redondeza,"
            "Isso ajuda a resolve-lo mais rápidamente."
        )
        return texto

def salvar_imagem(message):

    user_id = message.chat.id
    photo_id = message.photo[-1].file_id
    # Salvando o ID da foto no banco de dados
    photo_data = {"user_id": user_id,"photo_id": photo_id}
    return  {"user_id": user_id,"photo_id": photo_id}

   

            # Enviar mensagem de resposta

#v = verificar_endereco("São Paulo", "Ourinhos", 'Parque Gabriela', 'Alameda Manoel Angelo minucci')
#print(v)
