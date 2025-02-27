from flask import Blueprint, jsonify, request, json, render_template, redirect
from flask_login import login_required
from settings.extensions import mongo
from datetime import datetime, timedelta
from bson import json_util
import pytz


web_tp = Blueprint('web', __name__)


@web_tp.route('/web_tp', methods=['GET'])
def render_web_tp():
    return render_template('webhook.html')


@web_tp.route('/get_data', methods=['POST'])
def get_data():
    chave = request.form.get('chave')
    if not chave:
        return jsonify({"error": "O campo 'chave' é obrigatório"}), 400

    # Definir o fuso horário de São Paulo (Brasil)
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')

    # Calcular a data de 30 dias atrás no fuso horário de São Paulo
    trinta_dias_atras = datetime.now(sao_paulo_tz) - timedelta(days=30)

    # Buscar no MongoDB apenas os registros dentro dos últimos 30 dias
    pix_data = mongo.db.pix.find(
        {
            "chave": chave, 
            "recebido_em": {"$gte": trinta_dias_atras}  # Filtro usando 'recebido_em' ajustado para fuso horário de SP
        },
        {"_id": 0}  # Exclui o campo _id
    )
    return render_template("webhook_get.html", pix=pix_data)




@web_tp.route('/get_data_txid', methods=['POST'])
def get_data_txid():
    txid = request.form.get('txid')
    # Buscar dados do MongoDB
    pix_data = mongo.db.pix.find({"txid": txid}, {"_id": 0})

    return render_template("webhook_get.html", pix=pix_data)
