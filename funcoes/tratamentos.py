from keys import key
from unidecode import unidecode
#import keys as keys
api_key = key
def texto_padrao(boas_vindas=None, agradecimento=None, consulta=None):
    if boas_vindas:
       texto = str(
           "Vamos, lá...o que quer fazer no momento? clique em uma das opções abaixo ⬇️"
        )
       return texto

    
    elif agradecimento:
        texto = str(
            "Obrigado por ajudar a tornar nossa cidade um lugar melhor!\n\n"


            "Seu relato é extremamente importante para nós, pois nos ajuda a identificar áreas que precisam de melhorias e a tomar "
            "as medidas necessárias para resolver os problemas que afetam nossa comunidade"

            "Voce pode ver esse e outros problemas com mais detalhes, e de forma mais interativa futuramente, em uma plataforma que está sendo desenvolvida, não esqueça de compartilhar esse problemas com outros moradores da redondeza,"
            "Isso ajuda a resolve-lo mais rápidamente.\n\n"
            "clique aqui em /start, caso queira fazer mais alguma coisa por aqui.\n"
            "Caso tenha alguma sugestão, crítica ou opnião sobre o bot, fique a vontade para contatar os criadores."
            "contato para suporte: juniorsilvadavi42@gmail.com "

        )
        return texto

def salvar_imagem(message):
    user_id = message.chat.id
    photo_id = message.photo[-1].file_id
    # Salvando o ID da foto no banco de dados
    photo_data = {"user_id": user_id,
                  "photo_id": photo_id
                  }
    
    return photo_data