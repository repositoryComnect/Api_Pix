import requests
import settings.endpoints as endpoints, authenticate.utils as utils



def CobBoletoPost(data):
    token = utils.authenticateCobranca()

    url = f'{endpoints.URL_BOLETO_H}'

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    
    response = requests.post(url, headers=headers, json=data)

    return response