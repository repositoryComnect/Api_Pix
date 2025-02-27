import requests
import settings.endpoints as endpoints, authenticate.utils as utils
import jwt

# Cobrança imediata GET
def CobImediataGet(inicio, fim):
    token = utils.authenticate()
    url = f'{endpoints.URL_COBIMEDIATA_H}?inicio={inicio}&fim={fim}'
    
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)

    return response



# Cobrança imediata POST
def CobImediataPost(data):
    
    # Chama a função de autenticação
    token = utils.authenticate()

    # Obtem o endpoint
    url = f'{endpoints.URL_COBIMEDIATA_H}'
    #endpoints.URL_COBIMEDIATA_H 

    # Cabeçalhos da requisição
    headers = {
      'Authorization': f"Bearer {token}",
      'Content-Type': 'application/json'
        }

    
    # Envia a requisição
    response = requests.post(url, headers=headers, json=data)

    return response



# Cobrança imediata GET com Txid
def CobImediataTxidGet(id):
    token = utils.authenticate()
    url = f'{endpoints.URL_COBIMEDIATA_H}/{id}'
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)

    return response



# Cobrança imediata PUT com Txid
def CobImediataTxidPut(id, data):
    token = utils.authenticate()
    url = f'{endpoints.URL_COBIMEDIATA_H}/{id}'
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    response = requests.put(url, headers=headers, json=data)

    return response



# Cobrança imediata PATCH com Txid    
def CobImediataTxidPatch(id, data):
    token = utils.authenticate()
    url = f'{endpoints.URL_COBIMEDIATA_H}/{id}'
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    response = requests.patch(url, headers=headers, json=data)

    return response