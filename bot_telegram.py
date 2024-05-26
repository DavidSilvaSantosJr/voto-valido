import asyncio
import telebot
from telebot import types
import conexao_mongo
import funcoes.buscas, funcoes.consultas_maps, funcoes.tratamentos, funcoes.ia_gcp
import keys
from unidecode import unidecode
from datetime import datetime
api_key = keys.key 


bot = telebot.TeleBot(keys.CHAVE_API) #criação/conexão com a  chave api

# Função para lidar com o comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Relatar um problema que estou no local.')
    itembtn2 = types.KeyboardButton('Relatar um problema que vi, mas não estou no local.')
    itembtn3 = types.KeyboardButton('consultar relatos mais repercutidos da cidade.')
    itembtn4 = types.KeyboardButton('Encontrei um problema que foi resolvido!')
    markup.row(itembtn1, itembtn2)
    markup.row(itembtn3, itembtn4)
    bot.send_message(message.chat.id, funcoes.tratamentos.texto_padrao(boas_vindas=True) , reply_markup=markup)

user_data = {}

@bot.message_handler(func=lambda message: message.text == 'Relatar um problema que estou no local.')
def ask_location(message):
    chat_id = message.chat.id
    user_data['time'] = datetime.now()
    user_data['location'] = True
    user_data['state_problem'] = 'unsolved'
    user_data['state_location'] = 'gps'

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn = types.KeyboardButton('compartilhar Localização 📍', request_location=True)
    markup.add(itembtn)
    bot.send_message(chat_id, "Por favor, compartilhe sua localização atual, cicando no botão abaixo: ⬇️", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Relatar um problema que vi, mas não estou no local.')
def ask_location_sem_local(message):
    chat_id = message.chat.id
    user_data['time'] = datetime.now()
    user_data['location'] = True
    user_data['state_problem'] = 'unsolved'
    user_data['state_location'] = 'sem confirmacao'

    bot.send_message(chat_id, "Primeiro, envie UMA foto do problema: ")

@bot.message_handler(func=lambda message: message.text == 'Encontrei um problema que foi resolvido!')
def ask_location_sem_local(message):
    chat_id = message.chat.id
    user_data['state_problem'] = 'solved'
    bot.send_message(chat_id, "Que bacana!Agora preciso que você compartilhe sua localização, para identificar onde ele se encontra.")

@bot.message_handler(func=lambda message: message.text == 'consultar relatos mais repercutidos da cidade.')
def ask_location_sem_local(message):
    chat_id = message.chat.id
    user_data['state_location'] = False
    bot.send_message(chat_id, funcoes.tratamentos.texto_padrao(consulta=True))
    bot.send_message(chat_id, "Preciso que você envie o nome da cidade que quer buscar.\nUma dica: escreva corretamente, isso deixa a busca mais rápida 😉")

#tratamentos de mensagens
@bot.message_handler(content_types=['location'])
def ask_image(message):
    chat_id = message.chat.id
    if user_data['state_problem'] == 'solved':
        #busca a localização do problema
        #usa o id no mongo para localizar o problema do local
        #verifica a quanto tempo o probelma foi salvo (se for menor que uma semana,impossivel de ser consertado)
        #marca o problema como 'solved'
        pass
    if user_data['location'] == True:
        user_data['state_location'] = 'gps'
        coordenadas = [message.location.latitude, message.location.longitude]
        user_data['location'] = [message.location.latitude, message.location.longitude]
        array_local = funcoes.consultas_maps.salvar_uf_bairro_cidade(coordenadas) #capturar estado (uf) e  cidade
        user_data['uf'] = array_local[0].upper()
        user_data['city'] = array_local[1] 
        user_data['bairro'] = array_local[2].title()
        user_data['city_formated'] = unidecode(user_data['city'].lower())
        user_data['city_formated'] = user_data['city_formated'].replace("'", "")
        bot.send_message(chat_id, "Por favor, envie a foto do problema:")
    

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    chat_id = message.chat.id
    user_data['imagem'] = funcoes.tratamentos.salvar_imagem(message)
    bot.send_message(chat_id, "Agora de forma breve e resumida, descreva o problema:")


@bot.message_handler(func=lambda message: True and user_data['state_location'] == 'gps')
def save_data(message):
    chat_id = message.chat.id
    #verificar toxidade
    toxicidade = funcoes.ia_gcp.analise_texto_toxico(message.text)
    if toxicidade:
        bot.send_message(chat_id, "🤬 Opa! cuidado com as palavras, insira novamente a descrição.\nSeja cortez, ninguém gosta da falta de educação! 😉")

    if not toxicidade:
        user_data['descricao'] = message.text
        user_data['like'] = 0
        user_data['deslike'] = 0
        user_data['coments'] = {
            'time' : datetime.now(), #irá manipular formatos de data. Por isso a string
            'like' : int(),
            'deslike' : int(),
            'coment': str()
        }
 
        conexao_mongo.adicionar_dados(user_data)
        del user_data['_id'] 
        bot.send_message(chat_id, funcoes.tratamentos.texto_padrao(agradecimento=True))


#tratamento para localizçaõ inserida manualmente
@bot.message_handler(func=lambda message: True and user_data['state_location'] == 'sem confirmacao')
def save_data_longe(message): 
    chat_id = message.chat.id
    #verificar toxidade
    toxicidade = funcoes.ia_gcp.analise_texto_toxico(message.text)
    if toxicidade:
        user_data['state_location'] = 'sem confirmacao'
        bot.send_message(chat_id, "🤬 Opa! cuidado com as palavras, insira novamente a descrição.\nSeja cortez, ninguém gosta da falta de educação! 😉")
    
    else:
        user_data['state_location'] = 'confirmar localizacao'
        user_data['descricao'] = message.text
        bot.send_message(chat_id, 'Por fim, digite o endereço do local.\n\ndiga o estado, cidade, bairro e rua. Atente-se aos detalhes!')
    
@bot.message_handler(func=lambda message: True and user_data['state_location'] == 'confirmar localizacao')
def save_data_longe(message):
        chat_id = message.chat.id
        user_data['state_location'] = 'confirmar mapa'
        resultados = funcoes.consultas_maps.salvar_latlong_endereco(message.text)
        user_data['location'] = resultados[0], resultados[1]
        array_local = funcoes.consultas_maps.salvar_uf_bairro_cidade(resultados) #capturar estado (uf)
        user_data['uf'] = array_local[0].upper()
        user_data['city'] = array_local[1].title()
        user_data['bairro'] = array_local[2].title()
        user_data['city_formated'] = unidecode(user_data['city'].lower())
        user_data['city_formated'] = user_data['city_formated'].replace("'", "")
        bot.send_location(chat_id, resultados[0], resultados[1])

        markup = types.InlineKeyboardMarkup()
        sim_button = types.InlineKeyboardButton('Sim', callback_data='sim')
        nao_button = types.InlineKeyboardButton('Não', callback_data='nao')
        markup.row(sim_button, nao_button)
        # Envia a mensagem com o teclado de opções
        bot.send_message(chat_id, "verifique se é aqui onde o problema se encontra.", reply_markup=markup)
        bot.send_message(chat_id, "Você pode tocar no mapa e dar zoom, para ter mais precisão na verificação.")

@bot.callback_query_handler(func=lambda call: True and user_data['state_location'] == 'confirmar mapa')
def handle_callback_query(call):
    chat_id = call.message.chat.id
    if call.data == 'sim':
        user_data['state_location'] == 'manual'
        user_data['like'] = 0
        user_data['deslike'] = 0
        user_data['coments'] = {
            'time' : datetime.now(), #irá manipular formatos de data. Por isso a string
            'like' : int(),
            'deslike' : int(),
            'coment': str()
        }

        conexao_mongo.adicionar_dados(user_data)
        del user_data['_id'] 
        bot.send_message(chat_id, funcoes.tratamentos.texto_padrao(agradecimento=True))

    elif call.data == 'nao':
        user_data['state_location'] = 'confirmar localizacao'
        bot.send_message(chat_id, "Entendi. vamos tentar de novo, dessa vez, coloque mais detalhes, como bairro, cidade,nome da rua, ou até mesmo um n° rsidencial próximo.")
        


@bot.message_handler(func=lambda message: True and user_data['state_location'] == False)
def busca_Semana_consulta(message):
    resposta_busca = funcoes.buscas.resumo_semana(message.text)
    bot.send_message(message.chat.id, resposta_busca)

#problema concluido.

bot.polling()
