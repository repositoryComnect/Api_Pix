import requests
import flask, authenticate.utils as utils, settings.endpoints as endpoints



def ReqEnvioPut(data):
    token = utils.authenticate()

    url = f'{endpoints.URL_REQUISITAR_ENVIO_PIX_H}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.put(url, headers=headers, json=data)

    return response 




def ConsultarPixEnviadoGet(id):
    token = utils.authenticate()

    url = f'{endpoints.URL_REQUISITAR_ENVIO_PIX_H}/pix/enviados/{id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.put(url, headers=headers)

    return response 




def ConsultarPixEnviadoIdentGet(id):
    token = utils.authenticate()

    url = f'{endpoints.URL_REQUISITAR_ENVIO_PIX_H}/pix/enviados/id-envio/{id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.put(url, headers=headers)

    return response 




def ConsultarListaPixGet(inicio, fim):
    token = utils.authenticate()

    url = f'{endpoints.URL_REQUISITAR_ENVIO_PIX_H}/pix/enviados?inicio={inicio}&fim={fim}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.put(url, headers=headers)

    return response 




def DetalharQrcodePost(data):

    token = utils.authenticate()

    url = f'{endpoints.URL_REQUISITAR_ENVIO_PIX_H}/qrcodes/detalhar'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.put(url, headers=headers, json=data)

    return response 




def PagarQrcodePixPut(id, data):

    token = utils.authenticate()

    url = f'{endpoints.URL_REQUISITAR_ENVIO_PIX_H}/pix/{id}/qrcode'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type' : 'application/json'
    }

    response = requests.put(url, headers=headers, json=data)

    return response 