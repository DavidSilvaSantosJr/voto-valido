import conexao_mongo
import pymongo
import telebot
from telebot import types
from telebot import TeleBot, types
import funcoes.buscas, funcoes.consultas_maps, funcoes.tratamentos
import keys
from datetime import datetime
from problemas import dic_problemas, topicos, buscas, estados
from pprint import pprint

api_key = keys.key
bot = telebot.TeleBot(keys.CHAVE_API) #criação/conexão com a  chave api
client = pymongo.MongoClient(keys.STRING_CONNECTION)

user_data = {} # armazena chat_id do usuário, e ao consultar o chat_id para salavar, busca o id referente ao user, não ao escopo
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'chat_id':chat_id}
    print('dic inteiro:', user_data,'\ndic do user:',user_data[chat_id])

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn_no_local = types.KeyboardButton('Relatar um novo problema.')
    btn_solved = types.KeyboardButton('Encontrei um problema que foi resolvido!')
    btn_resumo = types.KeyboardButton('Consultar atualizações da minha cidade.')
    markup.row(btn_no_local)
    markup.row(btn_solved, btn_resumo)
    bot.send_message(message.chat.id, funcoes.tratamentos.texto_padrao(boas_vindas=True) , reply_markup=markup)
    

@bot.message_handler(func = lambda message: message.text == 'Relatar um novo problema.')
def relatar_novo_problema(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'time' : datetime.now()}
    conexao_mongo.adicionar_dados_incompletos(user_data[chat_id])
    print(user_data)
    bot.send_message(chat_id, 'envie uma foto do problema que você encontrou\nLembre-se, apenas UMA FOTO')

@bot.message_handler(func = lambda message: message.text == 'Consultar atualizações da minha cidade.')
def consulta_uf(message): 
    chat_id = message.chat.id
    user_data[chat_id] = {'consulta' : True}
    print(user_data)
    uf_distinct = funcoes.buscas.busca_local(uf=True)
    markup = types.InlineKeyboardMarkup()
    for uf in uf_distinct['uf']:
        uf_button = types.InlineKeyboardButton(uf, callback_data=uf)
        markup.row(uf_button)
    bot.send_message(chat_id, 'selecione o estado que deseja consultar', reply_markup=markup)

@bot.message_handler(func = lambda message: message.text == 'Encontrei um problema que foi resolvido!')
def problema_resolvido(message):
    bot.send_message(message.chat.id, 'Que ótimo!👍\n estamos desenvolvendo essa funcionalidade. Avisaremos asssim que possível😁🤝!')

    
"""    TRATAMENTO BOTÕES PRINCIPAIS PÓS START   """

@bot.message_handler(content_types=['photo', 'video', 'doc', 'audio', 'location'])
def salvar_types(message):
    chat_id = message.chat.id
    
    if message.content_type == 'photo':
      imagem = funcoes.tratamentos.salvar_imagem(message)
      user_data[chat_id]['imagem'] = imagem
      conexao_mongo.atualizar(user_data[chat_id]['_id'], user_data[chat_id])
      print(user_data)

      markup = types.InlineKeyboardMarkup()
      sim_button = types.InlineKeyboardButton('Sim', callback_data='sim_no_local')
      nao_button = types.InlineKeyboardButton('Não', callback_data='nao_no_local')
      markup.row(sim_button, nao_button)
      bot.send_message(chat_id, "Você está no local do problema?", reply_markup=markup)

    if message.content_type == 'location':
        coordenadas = [message.location.latitude, message.location.longitude]
        user_data[chat_id]['state_location'] = 'gps'
        try:
            user_data[chat_id]['localizacao'] = funcoes.consultas_maps.salvar_uf_bairro_cidade(coordenadas)
            conexao_mongo.atualizar(user_data[chat_id]['_id'], user_data[chat_id])
        except UnboundLocalError:
            bot.send_message(chat_id, "Ops, por favor, clique aqui em /start \nvamos tentar de novo, não achei o local.\n:( ")
        
        markup = types.InlineKeyboardMarkup()
        for topic in dic_problemas:
            btn_categoria = types.InlineKeyboardButton(topic, callback_data=topic)
            markup.row(btn_categoria)
        bot.send_message(chat_id, "Selecione abaixo uma categoria para o problema encontrado:", reply_markup=markup)
        
@bot.callback_query_handler(func=lambda call: call.data in ('nao_no_local','sim_no_local'))
def receber_localizacao(call):
    chat_id = call.message.chat.id
    if call.data == 'nao_no_local':
        user_data[chat_id]['state_location'] = 'manual'
        user_data[chat_id]['try_location'] = 1
        bot.send_message(chat_id, "Então escreva pra mim o local do problema\n\nInsira o estado, cidade, bairro e rua...\n\n")
        bot.send_message(chat_id, "Você também pode inserir o nome de um local, como: 'Escola x', 'praça da cidade','UPA da cidade'...")

    elif call.data == 'sim_no_local':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        itembtn = types.KeyboardButton('compartilhar Localização 📍', request_location=True)
        markup.add(itembtn)
        bot.send_message(chat_id, "Por favor, compartilhe sua localização atual, cicando no botão abaixo: ⬇️", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ('nao_mapa','sim_mapa'))
def verificar_local_no_mapa(call):
        chat_id = call.message.chat.id
        if call.data == 'sim_mapa':
            del user_data[chat_id]['try_location']
            markup = types.InlineKeyboardMarkup()
            for topic in dic_problemas:
                btn_categoria = types.InlineKeyboardButton(topic, callback_data=topic)
                markup.row(btn_categoria)
            bot.send_message(chat_id, "Selecione abaixo a categoria do problema encontrado", reply_markup=markup)

        if call.data == 'nao_mapa':
            del user_data[chat_id]['localizacao']
            bot.send_message(chat_id, "Entendi. vamos tentar de novo, dessa vez, coloque mais detalhes, como bairro, cidade,nome da rua, ou até mesmo um n° rsidencial próximo.")
            

"""         TRATAR MENSAGENS DE TEXTO"""
@bot.message_handler(func = lambda message: True)
def salvar_local_categoria(message):
    chat_id = message.chat.id

    #enviar mapa para confirmar localizacao
    if user_data[chat_id].get('try_location'):
        lat_long = funcoes.consultas_maps.salvar_latlong_endereco(message.text)
        bot.send_location(chat_id, lat_long[0], lat_long[1])
        user_data[chat_id]['localizacao'] = funcoes.consultas_maps.salvar_uf_bairro_cidade(lat_long)
        try:
            user_data[chat_id]['localizacao'] = funcoes.consultas_maps.salvar_uf_bairro_cidade(lat_long) #capturar estado (uf)
        except UnboundLocalError:
            bot.send_message(chat_id, "Ops, por favor, clique aqui em /start \nvamos tentar de novo, não achei o local.\n:( ")

        markup = types.InlineKeyboardMarkup()
        sim_button = types.InlineKeyboardButton('Sim', callback_data='sim_mapa')
        nao_button = types.InlineKeyboardButton('Não', callback_data='nao_mapa')
        markup.row(sim_button, nao_button)
        bot.send_message(chat_id, "É aqui que o problema se encontra?.\nVocê pode tocar no mapa e dar zoom, para ter mais precisão na verificação", reply_markup=markup)

    
    #verificar a seleção de categorias/adicionar no banco de dados
    if 'categoria' in user_data[chat_id]:
        user_data[chat_id]['sub_categoria'] = message.text
        user_data[chat_id]['state_atual'] = {'corrigido':False, 'analise':False, 'nao_corrigido':True}
        conexao_mongo.atualizar(user_data[chat_id]['_id'], user_data[chat_id])
        bot.send_message(message.chat.id, f"Pronto, já adicionamos o problema de {message.text} ao nosso sistema. 🤝🥳\n{funcoes.tratamentos.texto_padrao(agradecimento=True)}")
        conexao_mongo.adicionar_dados(user_data[chat_id])
        del user_data[chat_id]['_id']
        
    
    elif user_data[chat_id].get('consulta'):
        problemas_encontrados = funcoes.buscas.buscar_atualizacoes(message.text)
        bot.send_message(chat_id, problemas_encontrados)
    


#buscar categorias de problemas
@bot.callback_query_handler(func=lambda call: call.data in topicos)
def topic_selected(call):
    #buscar por categoria para exibir atualização
    chat_id = call.message.chat.id
    selected_topic = call.data
    user_data[chat_id]['categoria'] = selected_topic
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for subtopic in dic_problemas[selected_topic]:
        markup.add(types.KeyboardButton(subtopic))
    bot.send_message(call.message.chat.id, f"Agora selecione o tópico para dessa categoria: {selected_topic}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in buscas)
def atualizacao(call):
    chat_id = call.message.chat.id
    if call.data == 'busca_categoria':
        markup = types.InlineKeyboardMarkup()
        for topic in dic_problemas:
            btn_categoria = types.InlineKeyboardButton(topic, callback_data=topic)
            markup.row(btn_categoria)
        bot.send_message(chat_id, "Selecione abaixo qual categoria deseja ver: ", reply_markup=markup)


#busca de cidades por estados
@bot.callback_query_handler(func=lambda call: call.data in estados)
def buscar_cidade(call):
    print(user_data) 
    #user_data[chat_id]['consulta'] = True
    uf_to_agr = call.data
    chat_id = call.message.chat.id
    cidades = funcoes.buscas.busca_local(cidade=True, uf_to_agr=uf_to_agr)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    for cidade in cidades['cidades']:
        btn_categoria = types.KeyboardButton(cidade)
        markup.row(btn_categoria)
    bot.send_message(chat_id, "Selecione abaixo em qual cidade deseja fazer as consultas: ", reply_markup=markup)        



bot.polling()
