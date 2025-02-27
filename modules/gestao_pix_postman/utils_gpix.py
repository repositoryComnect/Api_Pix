import requests
import settings.endpoints as endpoints, authenticate.utils as utils


def GPixIdGet(e2eId):
    token = utils.authenticate()

    url = f'{endpoints.URL_GESTPIX_H}/{e2eId}'
        
        # Cabeçalhos da requisição
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)

    return response 

def GPixGet(inicio, fim):
    token = utils.authenticate()

    url = f'{endpoints.URL_GESTPIX_H}?inicio={inicio}&fim={fim}'
        
        # Cabeçalhos da requisição
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)

    return response

def GPixPut(e2eId, id, data):
    token = utils.authenticate()

    url = f'{endpoints.URL_GESTPIX_H}/{e2eId}/devolucao/{id}'

    headers = {
        'Authorization' : f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.put(url, headers=headers, json=data)

    return response 

def GPixe2eTdGet(e2eId, id):
    token = utils.authenticate()

    url = f'{endpoints.URL_GESTPIX_H}/{e2eId}/devolucao/{id}'

    headers = {
        'Authorization' : f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.put(url, headers=headers)

    return response 

