from flask import Blueprint, jsonify, request
import cob_imediata_postman.utils_cob as utils_cob, settings.error_messages as error_messages
from urllib.parse import quote

cob_imediata_pt = Blueprint('cob_imediata_postman', __name__)

## ------------------------------------------- Bloco Rotas Cobrança Imediata Postman--------------------------------------------------------------------------------------- ##

@cob_imediata_pt.route('/v2/cob', methods=['POST'])
def cob_imediata_post():
    if request.is_json:
        data = request.get_json()
        if not data:
            return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED}), 400

        calendario = data.get('calendario')
        valor = data.get('valor')
        chave = data.get('chave')

        if not calendario or not valor or not chave:
            return jsonify({'error': error_messages.ERROR_FIELD_MANDATORY}), 400
    
        response = utils_cob.CobImediataPost(data)

        return jsonify(response.json()), response.status_code
    else:
        return jsonify({'error': error_messages.ERROR_JSON_INVALIDO}), 400




# Consultar lista de cobranças
@cob_imediata_pt.route('/v2/cob', methods=['GET'])
def cob_imediata_get():
    # Obtém os parâmetros da URL
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')

    # Valida se os parâmetros foram passados
    if not inicio or not fim:
        return jsonify({'error': error_messages.ERROR_MISSING_PARAMETERS}), 400
    else:
        response = utils_cob.CobImediataGet(inicio, fim)

    # Redireciona para a rota get_cobrancas com os dados como parâmetros de consulta
    return jsonify(response.json()), response.status_code




# Consultar cobrança
@cob_imediata_pt.route('/v2/cob/<txid>', methods=['GET'])
def cob_imediata_txid_get(txid):
    # Valida se o parâmetro foi passado
    if not txid:
        return jsonify({'error': error_messages.ERROR_PARAMETER_TXID}), 400
    
    lenghtid = len(txid)

    if 26 <= lenghtid <= 35:
        # Código a ser executado se a condição for verdadeira
        response = utils_cob.CobImediataTxidGet(txid)

    return jsonify(response.json()), response.status_code

    



# Criar cobrança imediata (com txid)
@cob_imediata_pt.route('/v2/cob/<txid>', methods=['PUT'])
def cob_imediata_txid_put(txid):
    if request.is_json:
        data = request.get_json()
        # Valida se os parâmetros foram passados
        if not txid or not data:
            return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED}), 400
        
        calendario = data.get('calendario')
        valor = data.get('valor')
        chave = data.get('chave')
        lenghtid = len(txid)

        if not calendario or not valor or not chave:
            return jsonify({'error': error_messages.ERROR_FIELD_MANDATORY}), 400
        
        elif 26 <= lenghtid <= 35:
            response = utils_cob.CobImediataTxidPut(txid, data)
            return jsonify(response.json()), response.status_code
    else:
        return jsonify({'error': error_messages.ERROR_FORMATED_PAYLOAD}), 400



# Revisar cobrança
@cob_imediata_pt.route('/v2/cob/<id>', methods=['PATCH'])
def cob_imediata_txid_patch(id):
    data = request.get_json()
    lenghtid = len(id)
    # Valida se os parâmetros foram passados
    if not id or not data:
        return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED}), 400
    
    elif 26 <= lenghtid <= 35:
        response = utils_cob.CobImediataTxidPatch(id, data)

    return jsonify(response.json()), response.status_code
        