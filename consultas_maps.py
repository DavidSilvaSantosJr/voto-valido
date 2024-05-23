import requests
import unidecode
import json
from keys import key
api_key = key


def salvar_latlong_endereco(endereco):
    # Extrair informações da mensagem
    endereco = endereco.replace(" ", "%20")
    
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={endereco},Brasil&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
            data = json.loads(response.content)
            if  data["status"] == "OK":
                location = data ['results'][0]['geometry']['location']
                latitude = location['lat']
                longitude = location['lng']
                localizacao = [latitude, longitude]
                return localizacao
            
            elif data['status'] == "ZERO_RESULTS":
                resposta_busca = f"não consegui localizar {endereco.replace("%20", " ")}, verifique e tente novamente."
                return resposta_busca
            elif data['status'] == "INVALID_REQUEST":
                resposta_busca = f"Ops!, insira estado, cidade, bairro e rua, verifique e tente novamente."
                return resposta_busca

    else:
        print(response.status_code)


def salvar_uf_bairro_cidade(coordenadas): #list
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{coordenadas[0]},{coordenadas[1]}",
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        for result in data['results']:
            for component in result['address_components']:
                if 'administrative_area_level_1' in component['types']:
                    uf = component['short_name']

        for result in data['results']:
            for component in result['address_components']:
                if 'locality' in component['types']:
                    cidade = component["long_name"]
                    
        for result in data['results']:
            for component in result['address_components']:
                if ('political' or 'sublocality' or 'sublocality_level_1') in component['types']:
                    bairro = component['long_name']
                    return [uf, cidade, bairro]
                
    return "pane no sistema"
