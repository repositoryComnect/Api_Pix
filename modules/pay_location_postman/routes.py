from flask import Blueprint, jsonify, request
import pay_location_postman.utils_plocation as utils_plocation, settings.error_messages as error_messages

pay_location_pt = Blueprint('pay_location_pt', __name__)

## ------------------------------------------- Bloco Rotas Payload Locations ----------------------------------------------------------------------------- ##

@pay_location_pt.route('/v2/loc', methods=['GET'])
def pay_location_get():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')

    if not inicio or not fim:
        return jsonify({'error': error_messages.ERROR_MISSING_PARAMETERS}), 400
    else:
        response = utils_plocation.PayLocationGet(inicio, fim)

    return jsonify(response.json()), response.status_code





@pay_location_pt.route('/v2/loc', methods=['POST'])
def pay_location_post():
    data = request.get_json()
    tipocob = data.get('tipoCob')
    if not data:
        return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED}), 400
    if not tipocob:
        return jsonify({'error': error_messages.ERROR_FIELD_MANDATORY}), 400
    else:
        response = utils_plocation.PayLocationPost(data)

    return jsonify(response.json()), response.status_code




# ID deve ser numérico
@pay_location_pt.route('/v2/loc/<id>', methods=['GET'])
def pay_location_txid_get(id):
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID}), 400
    
    elif not id.isdigit() or not (1 <= len(id) <= 32):
        return jsonify({"error": error_messages.ERROR_NUMERIC_ID}), 400
    
    else:
        response = utils_plocation.PayLocationTxidGet(id)

    return jsonify(response.json()), response.status_code






@pay_location_pt.route('/v2/loc/<id>/qrcode', methods=['GET'])
def pay_location_id_qrcode_get(id):
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID}), 400
    
    elif not id.isdigit() or not (1 <= len(id) <= 32):
         return jsonify({"error": error_messages.ERROR_NUMERIC_ID}), 400
    
    else:
        response = utils_plocation.PayLocationTxidQrcodeGet(id)

    return jsonify(response.json()), response.status_code






@pay_location_pt.route('/v2/loc/<id>/txid', methods=['DELETE'])
def pay_location_id_delete(id):
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID}), 400
    
    elif not id.isdigit() or not (1 <= len(id) <= 32):
        return jsonify({"error": error_messages.ERROR_NUMERIC_ID}), 400
    
    else:
        response = utils_plocation.PayLocationIdDelete(id)

    return jsonify(response.json()), response.status_code

