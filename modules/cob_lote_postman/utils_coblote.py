import requests
import settings.endpoints as endpoints, authenticate.utils as utils


def CobLotePut(id, data):
    token = utils.authenticate()
    url = f'{endpoints.URL_COBLOTE_H}/{id}'
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    response = requests.put(url, headers=headers, json=data)

    return response 



def CobLotePatch(id, data):
    token = utils.authenticate()
    url = f'{endpoints.URL_COBLOTE_H}/{id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json' 
    }
    response = requests.patch(url, headers=headers, json=data)

    return response



def CobLoteIdGet(id):
    token = utils.authenticate()
    url = f'{endpoints.URL_COBLOTE_H}/{id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json' 
    }
    response = requests.get(url, headers=headers)

    return response



def CobLoteGet(inicio, fim):
    token = utils.authenticate()
    
    url = f'{endpoints.URL_COBLOTE_H}?inicio={inicio}&fim={fim}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json' 
    }
    response = requests.get(url, headers=headers)

    return response