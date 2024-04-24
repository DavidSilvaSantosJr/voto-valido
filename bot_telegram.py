import telebot
from telebot import types
import conexao_mongo
import funcoes.buscas
import funcoes.tratamentos
from unidecode import unidecode
import k
CHAVE_API = k.CHAVE_API
CHAVE_API_MAPS = k.CHAVE_API_MAPS


bot = telebot.TeleBot(CHAVE_API) #criação/conexão com a  chave api

# Função para lidar com o comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Expor um problema que estou no local.')
    itembtn2 = types.KeyboardButton('Expor um problema que vi, mas não estou no local.')
    itembtn3 = types.KeyboardButton('Resumo da ultima semana')
    itembtn4 = types.KeyboardButton('Visitar a plataforma, e ter mais detalhes!')
    markup.row(itembtn1, itembtn2)
    markup.row(itembtn3, itembtn4)
    bot.send_message(message.chat.id, funcoes.tratamentos.apresentacao() , reply_markup=markup)
    # Variáveis globais
data = None
user_data = {}
#localizado = True

@bot.message_handler(func=lambda message: message.text == 'Expor um problema que estou no local.')
def ask_location(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn = types.KeyboardButton('Enviar Localização', request_location=True)
    markup.add(itembtn)
    bot.send_message(message.chat.id, "Por favor, envie sua localização atual, cicando no botão abaixo:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Expor um problema que vi, mas não estou no local.')
def ask_location_sem_local(message):
    user_data['state_localizacao'] = 'sem confirmacao'
    bot.send_message(message.chat.id, "Por favor, envie uma imagem relacionada ao problema:")

@bot.message_handler(func=lambda message: message.text == 'visitar a plataforma, e ter um panorama geral!')
def ask_location_sem_local(message):
    bot.send_message(message.chat.id, "Você pode ver como anda a cidade em "
                                        "[link plataforma]")

@bot.message_handler(func=lambda message: message.text == 'Resumo da ultima semana')
def ask_location_sem_local(message):
    bot.send_message(message.chat.id, "insira o nome do estado")

@bot.message_handler(content_types=['location'])
def ask_image(message):
    user_data['state_localizacao'] = 'gps'
    latitude, longitude = message.location.latitude, message.location.longitude
    user_data['localizacao'] = [message.location.latitude, message.location.longitude]
    user_data['uf'] = funcoes.tratamentos.salvar_uf(latitude, longitude, CHAVE_API_MAPS) #capturar estado
    
    print(f"ESTADO -> {user_data['uf']}")
    print(user_data)    
    bot.send_message(message.chat.id, "Por favor, envie uma imagem relacionada ao problema:")

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    user_data['imagem'] = funcoes.tratamentos.salvar_imagem(message)
    bot.send_message(message.chat.id, "Por favor, descreva o problema:")
    print(user_data)


#armazena a descricao se ja tiver localização
@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == 'gps')
def save_data(message):   
    user_data['descricao'] = message.text
    conexao_mongo.adicionar_dados(user_data, user_data['uf'].title()) 
    bot.send_message(message.chat.id, f"Tudo ok! Você pode ver por esse e outros locais em [link plataforma]!")
    for k,v in user_data.items():
        print(k,' : ',v)

@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == 'sem confirmacao')
def save_data_longe(message): 
    if user_data['state_localizacao'] == 'sem confirmacao':
        user_data['state_localizacao'] = 'confirmar estado'
        user_data['descricao'] = message.text
        print(user_data)
        bot.send_message(message.chat.id, 'Digite o estado (UF)')
    

@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == 'confirmar estado')
def save_data_longe(message):
        user_data['state_localizacao'] = 'confirmar cidade'
        print(message.text)
        uf_pesquisa = message.text.title().replace(" ", "_")
        uf_pesquisa = unidecode(uf_pesquisa)
        user_data['estado'] = message.text
        busca = funcoes.buscas.consultar_estado(uf_pesquisa)
        print('procurar por estado: ',busca, 'enviado:', message.text) 
        bot.send_message(message.chat.id, f"Agora informe em qual cidade de {busca} você está.")
        user_data['localizacao'] = busca
        

@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == 'confirmar cidade')
def save_data_longe(message):
        user_data['state_localizacao'] = 'confirmar bairro'
        print(message.text)
        cidade_pesquisa = message.text.title().replace(" ", "_")
        cidade_pesquisa = unidecode(cidade_pesquisa)
        user_data['cidade'] = message.text
        busca = funcoes.buscas.consultar_cidade(cidade_pesquisa, user_data['localizacao'])
        print('procurar por cidade -> ',busca, 'enviado ->', message.text)
        bot.send_message(message.chat.id, f"Agora informe em qual bairro de {busca} você está.")

@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == 'confirmar bairro')
def save_data_longe(message):
    user_data['state_localizacao'] = 'confirmar rua'
    bairro_pesquisa = message.text.title().replace(" ", "_")
    bairro_pesquisa = unidecode(bairro_pesquisa)
    user_data['bairro'] = message.text
    print('procurar por bairro -> ',bairro_pesquisa, 'enviado ->', message.text)
    bot.send_message(message.chat.id, f"Agora informe em qual rua de {message.text} você está.")


@bot.message_handler(func=lambda message: True and user_data['state_localizacao'] == 'confirmar rua')
def save_data_longe(message):
    rua_pesquisa = message.text.title().replace(" ", "_")
    rua_pesquisa = unidecode(rua_pesquisa)
    user_data['rua'] = message.text
    print('procurar por bairro -> ',rua_pesquisa, 'enviado ->', message.text)
    bot.send_message(message.chat.id, f"Agora informe em qual rua de {message.text} você está.")
    
    estado = user_data['estado']
    municipio = user_data['cidade']
    bairro = user_data['bairro']
    rua = user_data['rua']

    resultados = funcoes.tratamentos.verificar_endereco(estado, municipio, bairro, rua)

    if resultados:
        # Processar os resultados da pesquisa
        for resultado in resultados:
            print(f"Nome: {resultado['name']}")
            print(f"Endereço: {resultado['formatted_address']}")
            print()

        else:
            print("Nenhum resultado encontrado.")

#r### tratar a localização enviada manulamente -- fazer a busca pelo nome do estado

bot.polling()
