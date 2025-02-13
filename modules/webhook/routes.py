from flask import Blueprint, jsonify, request, json, abort
import requests

webhook_wh = Blueprint('webhook_wh', __name__)

# Middleware para verificar o certificado do cliente APENAS para as rotas que exigem mTLS
'''@webhook_wh.before_request
def verificar_certificado():
    """
    Exige um certificado do cliente apenas para as rotas sensíveis.
    """
    if request.path in ["/webhook", "/pix", "/configWebhook"]:
        cert = request.environ.get("SSL_CLIENT_CERT")
        if not cert:
            abort(403, "Certificado de cliente obrigatório para este endpoint.")'''

# Rota básica do Webhook
@webhook_wh.route("/webhook", methods=["POST"])
def imprimir():
    print("Requisição recebida")
    print("Cabeçalhos:", request.headers)
    print("Corpo:", request.json)
    return jsonify({"status": 200, "message": "Webhook recebido com sucesso!"})

# Rota para manipular os dados do PIX
@webhook_wh.route("/pix", methods=["POST"])
def imprimirPix():
    data = request.json
    print(data)  # Apenas imprime os dados no terminal

    # Salva os dados recebidos em um arquivo
    with open('data.txt', 'a') as outfile:
        outfile.write("\n")
        json.dump(data, outfile)
        
    return jsonify({"status": 200, "message": "Dados do PIX recebidos e processados!"})

# Rota para configurar o Webhook no servidor da Efí
'''@webhook_wh.route("/configWebhook/<chave>", methods=["PUT"])
def config_webhook(chave):
    url = f"https://pix-h.api.efipay.com.br/v2/webhook/{chave}"

    headers = {
        'x-skip-mtls-checking': 'false'
    }

    params = {
        'chave': chave
    }

    body = {
        'webhookUrl': "https://efi.comnectlupa.com.br/webhook/"
    }

    response = requests.put(url, params=params, json=body, headers=headers)
    print(response)

    if response.status_code == 200:
        print("Webhook configurado com sucesso!")
    else:
        print(f"Erro ao configurar webhook: {response.status_code}")
        print(response.text)  # Mostra o conteúdo da resposta em caso de erro

    return response.text, response.status_code'''
