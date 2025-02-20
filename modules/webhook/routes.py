from flask import Blueprint, jsonify, request, json, abort
import requests
import hashlib
import hmac
import os

webhook_wh = Blueprint('webhook_wh', __name__)

# IP autorizado
AUTHORIZED_IP = '34.193.116.226'

# Chave secreta para gerar e verificar o HMAC
SECRET_KEY = os.environ.get("WEBHOOK_SECRET_KEY", "sua_chave_secreta")

# Função para verificar o IP de origem
'''def check_ip():
    ip = request.remote_addr
    if ip != AUTHORIZED_IP:
        print(f"IP não autorizado: {ip}")
        abort(403, description="IP não autorizado")

# Função para verificar o HMAC
def check_hmac():
    hmac_hash = request.args.get('hmac')
    if not hmac_hash:
        abort(400, description="HMAC não fornecido")

    # Gerar HMAC a partir da URL e da chave secreta
    url = request.url.split('?')[0]  # Ignora a parte query da URL
    computed_hmac = hmac.new(SECRET_KEY.encode(), url.encode(), hashlib.sha256).hexdigest()

    # Verificar se o HMAC recebido corresponde ao gerado
    if hmac_hash != computed_hmac:
        print(f"HMAC inválido. Esperado: {computed_hmac}, recebido: {hmac_hash}")
        abort(403, description="HMAC inválido")'''

# Rota básica do Webhook
@webhook_wh.route("/webhook", methods=["POST"])
def imprimir():
    # Verificar o IP de origem
    #check_ip()

    # Verificar o HMAC
    #check_hmac()

    print("Requisição recebida")
    print("Cabeçalhos:", request.headers)
    print("Corpo:", request.json)
    return jsonify({"status": 200, "message": "Webhook recebido com sucesso!"})

# Rota para manipular os dados do PIX
@webhook_wh.route("/webhook/pix", methods=["POST"])
def imprimirPix():
    # Verificar o IP de origem
    #check_ip()

    # Verificar o HMAC
    #check_hmac()

    data = request.json
    print(data)  # Apenas imprime os dados no terminal

    # Salva os dados recebidos em um arquivo
    with open('data.txt', 'a') as outfile:
        outfile.write("\n")
        json.dump(data, outfile)
        
    return jsonify({"status": 200, "message": "Dados do PIX recebidos e processados!"})
