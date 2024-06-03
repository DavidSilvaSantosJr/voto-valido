import asyncio
import conexao_mongo
import telebot
from telebot import types
from telebot import TeleBot, types
import funcoes.buscas, funcoes.consultas_maps, funcoes.tratamentos
import keys
from unidecode import unidecode
from datetime import datetime
from problemas import dic_problemas, topicos
from pprint import pprint
api_key = keys.key
bot = telebot.TeleBot(keys.CHAVE_API) #criação/conexão com a  chave api
global user_data
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    #usar o chat_id como nome do dicionario
    global nome_dict
    nome_dict = str(chat_id)
    nome_dict = {}
    markup = types.ReplyKeyboardMarkup()
    btn_no_local = types.KeyboardButton('Relatar um novo problema.')
    btn_solved = types.KeyboardButton('Encontrei um problema que foi resolvido!')
    markup.row(btn_no_local)
    markup.row(btn_solved)
    bot.send_message(message.chat.id, funcoes.tratamentos.texto_padrao(boas_vindas=True) , reply_markup=markup)
    

@bot.message_handler(func = lambda message: message.text == 'Relatar um novo problema.')
def relatar_novo_problema(message):
    nome_dict['time'] = datetime.now()
    chat_id = message.chat.id
    bot.send_message(chat_id, 'envie uma foto do problema que você encontrou\nLembe-se, apenas UMA FOTO')
    print(nome_dict)

@bot.message_handler(content_types=['photo', 'video', 'doc', 'audio', 'location'])
def salvar_types(message):
    chat_id = message.chat.id
    
    if message.content_type == 'photo':
      user_data['imagem'] = funcoes.tratamentos.salvar_imagem(message)
      markup = types.InlineKeyboardMarkup()
      sim_button = types.InlineKeyboardButton('Sim', callback_data='sim_no_local')
      nao_button = types.InlineKeyboardButton('Não', callback_data='nao_no_local')
      markup.row(sim_button, nao_button)
      bot.send_message(chat_id, "Você está no local do problema?", reply_markup=markup)

    if message.content_type == 'location':
        user_data['state_location'] = 'gps'
        coordenadas = [message.location.latitude, message.location.longitude]
        user_data['lat_long'] = [message.location.latitude, message.location.longitude]
        user_data['localizacao'] = funcoes.consultas_maps.salvar_uf_bairro_cidade(coordenadas)
        markup = types.InlineKeyboardMarkup()
        for topic in dic_problemas:
            global chave_codificada
            chave_codificada = topic
            btn_categoria = types.InlineKeyboardButton(topic, callback_data=chave_codificada)
            markup.row(btn_categoria)
        bot.send_message(chat_id, "Selecione abaixo uma categoria para o problema encontrado:", reply_markup=markup)
        ### bot.register_next_step_handler(call.message, escolher_categoria)
        
@bot.callback_query_handler(func=lambda call: call.data in ('nao_no_local','sim_no_local'))
def receber_localizacao(call):
    chat_id = call.message.chat.id
    if call.data == 'nao_no_local':
        bot.send_message(chat_id, "Então escreva pra mim o local do problema\n\nInsira o estado, cidade, bairro e rua...")
    elif call.data == 'sim_no_local':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        itembtn = types.KeyboardButton('compartilhar Localização 📍', request_location=True)
        markup.add(itembtn)
        bot.send_message(chat_id, "Por favor, compartilhe sua localização atual, cicando no botão abaixo: ⬇️", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ('nao_mapa','sim_mapa'))
def verificar_local_no_mapa(call):
        chat_id = call.message.chat.id
        if call.data == 'sim_mapa':
            markup = types.InlineKeyboardMarkup()
            for topic in dic_problemas:
                global chave_codificada
                chave_codificada = topic
                btn_categoria = types.InlineKeyboardButton(topic, callback_data=chave_codificada)
                markup.row(btn_categoria)
            bot.send_message(chat_id, "Selecione abaixo uma categoria para o problema encontrado", reply_markup=markup)
        ### bot.register_next_step_handler(call.message, escolher_categoria)

        if call.data == 'nao_mapa':
            bot.send_message(chat_id, "Entendi. vamos tentar de novo, dessa vez, coloque mais detalhes, como bairro, cidade,nome da rua, ou até mesmo um n° rsidencial próximo.")
            del user_data['lat_long']


@bot.message_handler(func = lambda message: True)
def salvar_local_categoria(message):
    chat_id = message.chat.id
    if not 'lat_long' in user_data:
        resultados = funcoes.consultas_maps.salvar_latlong_endereco(message.text)
        bot.send_location(chat_id, resultados[0], resultados[1])
        user_data['lat_long'] = resultados[0], resultados[1]
        user_data['localizacao'] = funcoes.consultas_maps.salvar_uf_bairro_cidade(resultados)
        try:
            user_data['localizacao'] = funcoes.consultas_maps.salvar_uf_bairro_cidade(resultados) #capturar estado (uf)
        except UnboundLocalError:
            bot.send_message(chat_id, "Ops, por favor, clique aqui em /start \nvamos tentar de novo, não achei o local.\n:( ")

        markup = types.InlineKeyboardMarkup()
        sim_button = types.InlineKeyboardButton('Sim', callback_data='sim_mapa')
        nao_button = types.InlineKeyboardButton('Não', callback_data='nao_mapa')
        markup.row(sim_button, nao_button)
        # Envia a mensagem com o teclado de opções
        bot.send_message(chat_id, "É aqui que o problema se encontra?.\nVocê pode tocar no mapa e dar zoom, para ter mais precisão na verificação", reply_markup=markup)
    #verificar a seleção de categorias/adicionar no banco de dados
    if 'categoria' in user_data:
        selected_subtopic = message.text
        user_data['sub_categoria'] = selected_subtopic
        bot.send_message(message.chat.id, f"Pronto, já adicionamos o problema de {selected_subtopic} ao nosso sistema. 🤝🥳")
        conexao_mongo.adicionar_dados(user_data)
        del user_data['_id']
        bot.send_message(chat_id, funcoes.tratamentos.texto_padrao(agradecimento=True))
        pprint(user_data)
        print()
#sub-tópicos selecionados.
@bot.callback_query_handler(func=lambda call: call.data in topicos)
def topic_selected(call):
    selected_topic = call.data
    user_data['categoria'] = selected_topic
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for subtopic in dic_problemas[selected_topic]:
        markup.add(types.KeyboardButton(subtopic))
    bot.send_message(call.message.chat.id, f"Onde melhor se classifica o problema de {selected_topic}", reply_markup=markup)


bot.polling()
