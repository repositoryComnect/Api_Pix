from flask import Blueprint, jsonify, request
import cob_lote.utils_coblote as utils_coblote, settings.error_messages as error_messages, requests

cob_lote_bp = Blueprint('cob_lote', __name__)
                        
@cob_lote_bp.route('/v2/lotecobv/<id>', methods=['PUT'])
def cob_lote_id_put(id):
    data = request.get_json()
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID}), 400
    
    elif not id.isdigit() or not (1 <= len(id) <= 32):
       return jsonify({"error": error_messages.ERROR_NUMERIC_ID}), 400
    
    else:
        response = utils_coblote.CobLotePut(id, data)

        # Verifica se a resposta é um JSON válido
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            return jsonify({'error': error_messages.ERROR_JSON_INVALIDO, 'response_text': response.text}), response.status_code

    return jsonify(response_json), response.status_code






@cob_lote_bp.route('/v2/lotecobv/<id>', methods=['PATCH'])
def cob_lote_id_patch(id):
    data = request.get_json()
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID}), 400
    
    elif not id.isdigit() or not (1 <= len(id) <= 32):
        return jsonify({"error": error_messages.ERROR_NUMERIC_ID}), 400

    else:
        response = utils_coblote.CobLotePatch(id, data)

    return jsonify(response.json()), response.status_code





@cob_lote_bp.route('/v2/lotecobv/<id>', methods=['GET'])
def cob_lote_id_get(id):
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID}), 400
    
    elif not id.isdigit() or not (1 <= len(id) <= 32):
       return jsonify({"error": error_messages.ERROR_NUMERIC_ID}), 400

    else:
        response = utils_coblote.CobLoteIdGet(id)

    return jsonify(response.json()), response.status_code




@cob_lote_bp.route('/v2/lotecobv', methods=['GET'])
def cob_lote_get():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID}), 400
    else:
        response = utils_coblote.CobLoteGet(inicio, fim)

    return jsonify(response.json()), response.status_code

