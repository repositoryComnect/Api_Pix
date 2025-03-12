from flask import Blueprint, jsonify, request
import requests, modules.cob_boleto_postman.utils_boleto as utils_boleto
from settings import error_messages



cob_boleto_pt = Blueprint('cob_boleto_pt', __name__)


@cob_boleto_pt.route('/v1/charge/one-step', methods=['POST'])
def cob_boleto_one_step_pt():
    if request.is_json:
        data = request.get_json()
        if not data:
            return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED})
        
        else:
            response = utils_boleto.CobBoletoOneStepPost(data)

            return jsonify(response.json()), response.status_code
    else:
        return jsonify({'error': error_messages.ERROR_JSON_INVALIDO})



@cob_boleto_pt.route('/v1/charge', methods=['POST'])
def cob_boleto_post_pt():
    if request.is_json:
        data = request.get_json()
        print(data)
        if not data:
            return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED})
        
        else:
            response = utils_boleto.CobBoletoPost(data)

            return jsonify(response.json()), response.status_code
    else:
        return jsonify({'error': error_messages.ERROR_JSON_INVALIDO})
    



@cob_boleto_pt.route('/v1/charge/<id>/pay', methods=['POST'])
def cob_boleto_post_id_pt():

    return


@cob_boleto_pt.route('/v1/charge/<id>', methods=['GET'])
def cob_boleto_get_id_pt():

    return


@cob_boleto_pt.route('/v1/charges', methods=['GET'])
def cob_boleto_get_pt():
    
    return


