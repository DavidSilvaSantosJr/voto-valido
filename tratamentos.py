import requests
import unidecode
import json
import k

def apresentacao():
    texto = str(
        "Olá! sou o Veve, o bot que vai ajudar a cidade.\n\n"
        "Diga onde está o problema, envie uma foto e descreva o que está acontecendo ali.\n\n\n"
        "Ah, e mesmo que você esteja longe do local do problema, é possivel adiciona-lo na plataforma. Caso não tenha a imagem"
        "basta enviar o link para alguém que esteja por lá.\n\n\n"
        "Siga as instruções, e seja bem vindo!\n"
        "caso eu pare, ou não dê respostas, clique em /start, e o processo será refeito"

    )
    return texto
def salvar_latitude(lat, long):
    latitude, longitude = lat, long
    return [latitude, longitude]

def salvar_lating(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']

        return latitude, longitude

def salvar_uf(latitude, longitude, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{latitude},{longitude}",
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        for result in data['results']:
            for component in result['address_components']:
                if 'administrative_area_level_1' in component['types']:
                    uf = component['long_name'].title()
                    uf = unidecode.unidecode(uf)
                    return uf
    return "pane no sistema pipipipipipiiiii"
    

def salvar_imagem(message):

    user_id = message.chat.id
    photo_id = message.photo[-1].file_id
    # Salvando o ID da foto no banco de dados
    photo_data = {"user_id": user_id,"photo_id": photo_id}
    return  {"user_id": user_id,"photo_id": photo_id}

   
def verificar_endereco(estado, municipio, bairro, rua):
  """
  Verifica se um endereço existe no Google Maps.

  Args:
    estado: O nome do estado.
    municipio: O nome do município.
    bairro: O nome do bairro.
    nome_rua: O nome da rua.

  Returns:
    Uma lista de resultados da pesquisa da API do Google Maps.
  """

  # Codificar os parâmetros da URL
  url_encoded_estado = requests.utils.quote(estado)
  url_encoded_municipio = requests.utils.quote(municipio)
  url_encoded_bairro = requests.utils.quote(bairro)
  url_encoded_nome_rua = requests.utils.quote(rua)

  # Criar a URL da solicitação para a API do Google Maps
  url = f"https://maps.googleapis.com/maps/api/place/findtextsearch/json?key={k.CHAVE_API_MAPS}&address={url_encoded_nome_rua},{url_encoded_bairro},{url_encoded_municipio},{url_encoded_estado}&type=street_address"

  # Enviar a solicitação e obter a resposta
  response = requests.get(url)

  # Verificar se a solicitação foi bem-sucedida
  if response.status_code == 200:

    # Decodificar a resposta JSON
    data = json.loads(response.content)

    # Retornar os resultados da pesquisa
    return data['results']

  else:

    # Erro na solicitação
    raise Exception(f"Erro na solicitação da API do Google Maps: {response.status_code}")

