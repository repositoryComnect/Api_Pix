from flask import Blueprint, jsonify, request
import gestao_pix.utils_gpix as utils_gpix, settings.error_messages as error_messages

gest_pix_bp = Blueprint('gest_pix', __name__)

## ------------------------------------------- Bloco Rotas Gestão de Pix ----------------------------------------------------------------------------- ##

@gest_pix_bp.route('/v2/pix/<e2eId>', methods=['GET'])
def gest_pix_id_get(e2eId):
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_E2EID}), 400
    length = len(e2eId)

    if length < 32:
        return jsonify({'error': error_messages.ERROR_LENGTH_PARAMETER}), 400
    else:
        response = utils_gpix.GPixIdGet(e2eId)

    return jsonify(response.json()), response.status_code



@gest_pix_bp.route('/v2/pix', methods=['GET'])
def gest_pix_get():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')

    # Valida se os parâmetros foram passados
    if not inicio or not fim:
        return jsonify({'error': error_messages.ERROR_MISSING_PARAMETERS}), 400
    else:
        response = utils_gpix.GPixGet(inicio, fim)

    return jsonify(response.json()), response.status_code





@gest_pix_bp.route('/v2/pix/<e2eId>/devolucao/<id>', methods=['PUT'])
def gest_pix_put(e2eId, id):
    data = request.get_json()
    valor = data.get('valor')
    if not id or not e2eId:
        return jsonify({'error': error_messages.ERROR_PARAMETERS}), 400
    
    if not data:
        return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED}), 400
    
    if not valor:
        return jsonify({'error': error_messages.ERROR_PARAMETERS}), 400
    
    else:
        response = utils_gpix.GPixPut(e2eId, id, data)

    return jsonify(response.json()), response.status_code





@gest_pix_bp.route('/v2/pix/<e2eId>/devolucao/<id>', methods=['GET'])
def gest_pix_devolucao_id_get(e2eId, id):
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID}), 400
    
    length = len(e2eId)

    if length < 32:
        return jsonify({'error': error_messages.ERROR_LENGTH_PARAMETER}), 400

    else:
        response = utils_gpix.GPixe2eTdGet(e2eId, id)

    return jsonify(response.json()), response.status_code

