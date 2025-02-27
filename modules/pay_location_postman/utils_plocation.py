import requests
import settings.endpoints as endpoints, authenticate.utils as utils


def PayLocationGet(inicio, fim):
    token = utils.authenticate()
    url = f'{endpoints.URL_PAYLOCATIONS_H}?inicio={inicio}&fim={fim}'
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)

    return response





def PayLocationPost(data):
    token = utils.authenticate()
    url = endpoints.URL_PAYLOCATIONS_H
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)

    return response





def PayLocationTxidGet(id):
    token = utils.authenticate()
    url = f'{endpoints.URL_PAYLOCATIONS_H}/{id}'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }
    response = requests.get(url, headers=headers)

    return response






def PayLocationTxidQrcodeGet(id):
    token = utils.authenticate()
    url = f'{endpoints.URL_PAYLOCATIONS_H}/{id}/qrcode'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.get(url, headers=headers)

    return response






def PayLocationIdDelete(id):
    token = utils.authenticate()
    url = f'{endpoints.URL_PAYLOCATIONS_H}/{id}/txid'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.delete(url, headers=headers)

    return response 
