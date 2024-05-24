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
user_data = {}

# Função para lidar com o comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    btn_no_local = types.KeyboardButton('Relatar um problema que estou no local.')
    btn_fora_local = types.KeyboardButton('Relatar um problema que vi, mas não estou no local.')
    btn_relatos = types.KeyboardButton('Consultar relatos mais repercutidos da cidade.')
    btn_solved = types.KeyboardButton('Encontrei um problema que foi resolvido!')
    markup.row(btn_no_local, btn_fora_local)
    markup.row(btn_relatos, btn_solved)
    bot.send_message(message.chat.id, funcoes.tratamentos.texto_padrao(boas_vindas=True) , reply_markup=markup)

    #receber localizacao
@bot.message_handler(func=lambda message: message.text == 'Relatar um problema que estou no local.')
def receber_localizacao(message):
    chat_id = message.chat.id
    user_data['time'] = datetime.now()
    user_data['momento'] = 'nao_resolvido'
    user_data['modo_localizacao'] = 'compartilhada'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn = types.KeyboardButton('compartilhar Localização 📍', request_location=True)
    markup.add(itembtn)
    bot.send_message(chat_id, "Por favor, compartilhe sua localização atual, cicando no botão abaixo: ⬇️", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Relatar um problema que vi, mas não estou no local.')
def receber_localizacao_manualmente(message):
    chat_id = message.chat.id
    user_data['time'] = datetime.now()
    user_data['momento'] = 'nao_resolvido'
    user_data['modo_localizacao'] = 'inserida_manualmente'
    bot.send_message(chat_id, 'Por favor, digite o endereço do local.\n\nDiga o estado, cidade, bairro e rua. Atente-se aos detalhes!')

@bot.message_handler(func=lambda message: True and user_data['modo_localizacao'] == 'inserida_manualmente' and 'imagem' not in user_data)
def guardar_localizacao_manualmente(message):
    chat_id = message.chat.id
    resultados = funcoes.consultas_maps.salvar_latlong_endereco(message.text)
    user_data['result_pesquisa'] = resultados
    bot.send_location(chat_id, resultados[0], resultados[1])

    markup = types.InlineKeyboardMarkup()
    sim_button = types.InlineKeyboardButton('Sim', callback_data='sim')
    nao_button = types.InlineKeyboardButton('Não', callback_data='nao')
    markup.row(sim_button, nao_button)
    # Envia a mensagem com o teclado de opções
    bot.send_message(chat_id, "verifique se é aqui onde o problema se encontra.", reply_markup=markup)
    bot.send_message(chat_id, "Você pode tocar no mapa e dar zoom, para ter mais precisão na verificação.")
    
@bot.callback_query_handler(func=lambda call: True and user_data['modo_localizacao'] == 'inserida_manualmente')
def handle_callback_query(call):
    chat_id = call.message.chat.id
    if call.data == 'sim':
            resultados = user_data['result_pesquisa']
            user_data['location'] = [resultados[0], resultados[1]]
            array_local = funcoes.consultas_maps.salvar_uf_bairro_cidade(resultados) #capturar estado (uf)
            user_data['uf'] = array_local[0].upper()
            user_data['city'] = array_local[1].title()
            user_data['bairro'] = array_local[2].title()
            user_data['city_formated'] = unidecode(user_data['city'].lower())
            user_data['city_formated'] = user_data['city_formated'].replace("'", "")
            user_data['like'] = 0
            user_data['deslike'] = 0
            user_data['coments'] = {
            'time' : datetime.now(), #irá manipular formatos de data. Por isso a string
            'like' : int(),
            'deslike' : int(),
            'coment': str()
            }
            del user_data['result_pesquisa']
            bot.send_message(chat_id, "Agora, envie UMA foto do problema.")
            
    elif call.data == 'nao':
        bot.send_message(chat_id, "Entendi. vamos tentar de novo, dessa vez, coloque mais detalhes, como bairro, cidade,nome da rua, ou até mesmo um n° rsidencial próximo.")

@bot.message_handler(content_types=['location', 'photo', 'video', 'audio', 'document'])
def guardar_types(message):
    chat_id = message.chat.id
    if message.content_type == 'location':
        chat_id = message.chat.id
        coordenadas = [message.location.latitude, message.location.longitude]
        user_data['location'] = [message.location.latitude, message.location.longitude]
        array_local = funcoes.consultas_maps.salvar_uf_bairro_cidade(coordenadas) #capturar estado (uf) e  cidade
        user_data['uf'] = array_local[0].upper()
        user_data['city'] = array_local[1] 
        user_data['bairro'] = array_local[2].title()
        user_data['city_formated'] = unidecode(user_data['city'].lower())
        user_data['city_formated'] = user_data['city_formated'].replace("'", "")
        user_data['like'] = 0
        user_data['deslike'] = 0
        user_data['coments'] = {
        'time' : datetime.now(), #irá manipular formatos de data. Por isso a string
        'like' : int(),
        'deslike' : int(),
        'coment': str()
        }
        bot.send_message(chat_id, "Por favor, envie uma foto do problema:")

    if message.content_type == 'photo':
        user_data['imagem'] = funcoes.tratamentos.salvar_imagem(message)
        print(user_data)
        bot.send_message(chat_id, "Agora de forma breve e resumida, descreva o problema:")
    if message.content_type not in ['location', 'photo']:
        bot.send_message(chat_id, "Opá! só trabalho com texto e imagens, envie apenas uma foto do problema!")

@bot.message_handler(func=lambda message: True and 'imagem' in user_data)
def save_data_longe(message): 
    chat_id = message.chat.id
    #verificar toxidade
    toxicidade = funcoes.ia_gcp.analise_texto_toxico(message.text)
    if toxicidade:
        bot.send_message(chat_id, "🤬 Opa! cuidado com as palavras, insira novamente a descrição.\nSeja cortez, ninguém gosta da falta de educação! 😉")
    
    else:
        bot.send_message(chat_id, "Só 1 minuto...estou anotando as informações...")
        user_data['descricao'] = message.text
        conexao_mongo.adicionar_dados(user_data)
        del user_data['_id'] 
        bot.send_message(chat_id, funcoes.tratamentos.texto_padrao(agradecimento=True))
        user_data = {}

bot.polling()
