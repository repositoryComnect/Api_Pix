import requests
import base64
from settings.credentials import credentials
import settings.endpoints as endpoints
import random
import string


# Função que autentica e retorna o token 
def authenticate():
    try:
        # Codifica as credenciais em Base64
        auth = base64.b64encode(
            f"{credentials['client_id']}:{credentials['client_secret']}".encode()
        ).decode()
        
        # URL do endpoint
        url = endpoints.AUTH_URL_H
        # Corpo da requisição
        payload = '{"grant_type": "client_credentials"}'
        
        # Cabeçalhos da requisição
        headers = {
            'Authorization': f"Basic {auth}",
            'Content-Type': 'application/json'
        }
        # Envia a requisição
        response = requests.post(url, headers=headers, data=payload, cert=credentials['certificate'])
        # Verifica o status da resposta
        if response.status_code != 200:
            print("Erro ao obter o token:", response.text)  # Para fins de depuração
            return None  # Retorna None em caso de erro
        
        # Converte a resposta para JSON
        response_data = response.json()
        # Captura o token
        access_token = response_data.get('access_token')
        return access_token  # Retorna apenas o token

    except Exception as e:
        print("Erro durante a autenticação:", str(e))  # Para fins de depuração
        return None
    

    

# Função que cria um TxID para criação de cobranças com vencimento
def CreateTxid(lengh=26):
    if lengh < 26 or lengh > 35:
        raise ValueError("O tamanho deve estar entre 26 e 35 caracteres.")
    caracteres = string.ascii_letters + string.digits  # Letras e números
    return ''.join(random.choices(caracteres, k=lengh))




# Função que cria um E2eID para gerenciamento de Pix 
def CreateE2eid():
    caracteres = string.ascii_letters + string.digits  # Letras e números
    return ''.join(random.choices(caracteres, k=32))



def authenticateCobranca():
    try:
        auth = base64.b64encode(
        (f"{credentials['client_id']}:{credentials['client_secret']}").encode()).decode()

        url = endpoints.AUTH_URL_COB_H  #Para ambiente de Desenvolvimento

        payload="{\r\n    \"grant_type\": \"client_credentials\"\r\n}"
        headers = {
        'Authorization': f"Basic {auth}",
        'Content-Type': 'application/json'
        }

        response = requests.request("POST",
                                url,
                                headers=headers,
                                data=payload)
        
        response_data = response.json()
            # Captura o token

        access_token = response_data.get('access_token')

        return access_token  # Retorna apenas o token
    
    except Exception as e:
        print("Erro durante a autenticação:", str(e))  # Para fins de depuração
        return None

    