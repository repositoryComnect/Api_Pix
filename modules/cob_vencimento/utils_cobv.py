import requests
import settings.endpoints as endpoints, authenticate.utils as utils


def CobVencimentoGet(inicio, fim):
# Chama a função authenticate
    token = utils.authenticate()
    
    # Obtém o endpoint e inclui os parâmetros de consulta na URL
    url = f"{endpoints.URL_COBVENCIMENTO_H}?inicio={inicio}&fim={fim}"

    # Cabeçalhos da requisição
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    # Envia a requisição
    response = requests.get(url, headers=headers)

    return response

    
def CobVencimentoTxidGet(id):
# Chama a função authenticate
    token = utils.authenticate()
    
    # Obtém o endpoint e inclui os parâmetros de consulta na URL
    url = f"{endpoints.URL_COBVENCIMENTO_H}/{id}"

    # Cabeçalhos da requisição
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    # Envia a requisição
    response = requests.get(url, headers=headers)

    return response

def CobVencimentoTxidPut(id, data):
    token = utils.authenticate()
    url = f'{endpoints.URL_COBVENCIMENTO_H}/{id}'

    headers = {
        'Authorization': f'Bearer {token}', 
        'Content-Type': 'application/json'
    }

    response = requests.put(url, headers=headers, json=data)
    
    return response

def CobVencimentoTxidPatch(id, data):
    token = utils.authenticate()
    url = f'{endpoints.URL_COBVENCIMENTO_H}/{id}'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }
    response = requests.patch(url, headers=headers, json=data)

    return response