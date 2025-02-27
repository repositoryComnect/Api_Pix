from flask import Blueprint, jsonify, request, json, abort
import requests
import hashlib
import hmac
import os
from datetime import datetime
from settings.extensions import mongo
from settings.credentials import Config
from pymongo import MongoClient
import pytz

webhook_wh = Blueprint('webhook_wh', __name__)

# Conexão com o MongoDB usando a URI
client = MongoClient(Config.MONGO_URI)

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

    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    
    # Obtém a data atual no fuso horário de São Paulo
    data_brasil = datetime.now(sao_paulo_tz)

    # Converte a data para UTC antes de persistir
    data_utc = data_brasil.astimezone(pytz.utc)

    if "pix" in data:
        for pagamento in data["pix"]:
            documento = {
                "chave": pagamento["chave"],
                "endToEndId": pagamento["endToEndId"],
                "horario": pagamento["horario"],
                "infoPagador": pagamento["infoPagador"],
                "txid": pagamento["txid"],
                "valor": float(pagamento["valor"]),  # Convertendo para número
                "recebido_em": data_utc  # Timestamp de quando foi salvo no banco
            }

            try:
                mongo.db.pix.insert_one(documento)
                client.close()
                print("Documento inserido com sucesso!")
            except Exception as e:
                print(f"Erro ao inserir documento: {e}")

        
    return jsonify({"status": 200, "message": "Dados do PIX recebidos e processados!"})


