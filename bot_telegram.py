import telebot
from telebot import types
import conexao_mongo
import unidecode
import funcoes.buscas, funcoes.consultas_maps, funcoes.tratamentos
import keys
api_key = keys.key 


bot = telebot.TeleBot(keys.CHAVE_API) #criação/conexão com a  chave api

# Função para lidar com o comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Relatar um problema que estou no local.')
    itembtn2 = types.KeyboardButton('Relatar um problema que vi, mas não estou no local.')
    itembtn3 = types.KeyboardButton('Resumo da última semana')
    itembtn4 = types.KeyboardButton('Visitar a plataforma, e ter mais detalhes!')
    markup.row(itembtn1, itembtn2)
    markup.row(itembtn3, itembtn4)
    bot.send_message(message.chat.id, funcoes.tratamentos.apresentacao() , reply_markup=markup)
    # Variáveis globais
data = None
user_data = {}
#localizado = True

@bot.message_handler(func=lambda message: message.text == 'Relatar um problema que estou no local.')
def ask_location(message):
    user_data['data_hora'] = message.date
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn = types.KeyboardButton('Enviar Localização', request_location=True)
    markup.add(itembtn)
    bot.send_message(message.chat.id, "Por favor, envie sua localização atual, cicando no botão abaixo:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Relatar um problema que vi, mas não estou no local.')
def ask_location_sem_local(message):
    user_data['data_hora'] = message.date
    user_data['state_localizacao'] = 'sem confirmacao'
    bot.send_message(message.chat.id, "Por favor, envie a foto do problema:")

@bot.message_handler(func=lambda message: message.text == 'visitar a plataforma, e ter um panorama geral!')
def ask_location_sem_local(message):
    bot.send_message(message.chat.id, "Você pode ver como anda a cidade em "
                                        "[link plataforma]")

@bot.message_handler(func=lambda message: message.text == 'Resumo da última semana')
def ask_location_sem_local(message):
    user_data['state_localizacao'] = False
    bot.send_message(message.chat.id, "insira o nome do estado: ")

@bot.message_handler(content_types=['location'])
def ask_image(message):
    user_data['state_localizacao'] = 'gps'
    coordenadas = [message.location.latitude, message.location.longitude]
    user_data['localizacao'] = [message.location.latitude, message.location.longitude]
    array_local = funcoes.consultas_maps.salvar_uf(coordenadas) #capturar estado (uf) e  cidade
    user_data['uf'] = array_local[0].upper()
    user_data['cidade'] = array_local[1]
    print(user_data)    
    bot.send_message(message.chat.id, "Por favor, envie a foto do problema:")

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    user_data['imagem'] = funcoes.tratamentos.salvar_imagem(message)
    bot.send_message(message.chat.id, "Por favor, descreva o problema:")
    print(user_data)

@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == 'gps')
def save_data(message):
    user_data['descricao'] = message.text
    conexao_mongo.adicionar_dados(user_data, user_data['uf']) 
    bot.send_message(message.chat.id, f"Tudo ok! Você pode ver por esse e outros locais em [link plataforma]!")
    for k,v in user_data.items():
        print(k,' : ',v)

#armazena a descricao se ja tiver localização
@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == 'sem confirmacao')
def save_data_longe(message): 
    user_data['state_localizacao'] = 'confirmar localizacao'
    user_data['descricao'] = message.text
    print(user_data)
    bot.send_message(message.chat.id, 'insira o endereço do local.')
    bot.send_message(message.chat.id, 'diga o estado, cidade, bairro e rua. Atente-se aos detalhes!')
    

@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == 'confirmar localizacao')
def save_data_longe(message):
        user_data['state_localizacao'] = 'confirmar mapa'
        print(message.text)
        resultados = funcoes.consultas_maps.verificar_endereco(message.text)
        user_data['localizacao'] = resultados[0], resultados[1]
        array_local = funcoes.consultas_maps.salvar_uf(resultados) #capturar estado (uf)
        user_data['uf'] = array_local[0].upper()
        user_data['cidade'] = array_local[1].title()
        print(user_data)
        bot.send_location(message.chat.id, resultados[0], resultados[1])

        markup = types.InlineKeyboardMarkup()
        sim_button = types.InlineKeyboardButton('Sim', callback_data='sim')
        nao_button = types.InlineKeyboardButton('Não', callback_data='nao')
        markup.row(sim_button, nao_button)
        # Envia a mensagem com o teclado de opções
        bot.send_message(message.chat.id, "verifique se é aqui que o problema se encontra.", reply_markup=markup)
        bot.send_message(message.chat.id, "Você pode tocar no mapa e dar zoom, para ter mais precisão na verificação.")

@bot.callback_query_handler(func=lambda call: True and user_data['state_localizacao'] == 'confirmar mapa')
def handle_callback_query(call):
    if call.data == 'sim':
        user_data['state_localizacao'] == 'manual'
        conexao_mongo.adicionar_dados(user_data, user_data['uf'])
        bot.send_message(call.message.chat.id, f"Tudo ok! Você pode ver por esse e outros locais em [link plataforma]!")

    elif call.data == 'nao':
        user_data['state_localizacao'] = 'confirmar localizacao'
        bot.send_message(call.message.chat.id, "Entendi. vamos tentar de novo, dessa vez, coloque mais detalhes, como bairro, cidade,nome da rua, pu até mesmo um n° rsidencial próximo.")


buscas = []
@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == False)
def busca_Semana(message):
    user_data['state_localizacao'] = True
    bot.send_message(message.chat.id, "Agora a cidade")
    uf_consulta = message.text.upper()
    uf_consulta = unidecode.unidecode(uf_consulta)
    buscas.append(uf_consulta)

@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == True)
def busca_Semana_consulta(message):
    user_data['state_busca'] = 'aguardando buscas'
    cidade_consulta = message.text.title()
    buscas.append(cidade_consulta)

    bot.send_message(message.chat.id, f"esses foram os últimos acontecimentos da sesmana em {message.text}:")
    resposta_busca = funcoes.buscas.resumo_semana(buscas[0], buscas[1])
    bot.send_message(message.chat.id, resposta_busca)


bot.polling()
