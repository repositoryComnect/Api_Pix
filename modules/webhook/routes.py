from flask import Blueprint, jsonify, request, json

webhook_wh = Blueprint('webhook', __name__)

# Rota básica do Webhook
@webhook_wh.route("/webhook", methods=["POST"])
def imprimir():
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
