from flask import Blueprint, jsonify, request
import envio_pagamento_pix.utils_envio_pagamento as utils_envio_pagamento, settings.error_messages as error_messages


env_pagamento_pix_bp = Blueprint('env_pagamento_pix', __name__)

# Necessário finalizar
@env_pagamento_pix_bp.route('/v3/gn/pix/', methods=['PUT'])
def requisitar_envio_pix_put():
    data = request.get_json()
    if not data:
        return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED})
    else:
        response = utils_envio_pagamento.ReqEnvioPut(data)

    return jsonify(response.json()), response.status_code




# Necessário finalizar
@env_pagamento_pix_bp.route('/v2/gn/pix/enviados/<id>', methods=['GET'])
def consultar_pix_enviado_get(id):
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID})
    else:
        response = utils_envio_pagamento.ConsultarPixEnviadoGet(id)
    return jsonify(response.json()), response.status_code



# Necessário finalizar
@env_pagamento_pix_bp.route('/v2/gn/pix/enviados/id-envio/<id>', methods=['GET'])
def consultar_pix_enviado_identificador_get(id):
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_ID})
    else:
        response = utils_envio_pagamento.ConsultarPixEnviadoIdentGet(id)

    return jsonify(response.json()), response.status_code




# Necessário finalizar
@env_pagamento_pix_bp.route('/v2/gn/pix/enviados', methods=['GET'])
def consultar_lista_pix():
    inicio = request.get_data('inicio')
    fim = request.get_data('fim')

    if not inicio and fim:
        return jsonify({'error': error_messages.ERROR_MISSING_PARAMETERS})
    else:
        response = utils_envio_pagamento.ConsultarListaPixGet(inicio, fim)
        
    return jsonify(response.json()), response.status_code



# Necessário finalizar
@env_pagamento_pix_bp.route('/v2/gn/qrcodes/detalhar', methods=['POST'])
def detalhar_qrcode_pix():
    data = request.get_data()
    if not data:
        return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED})
    else:
        response = utils_envio_pagamento.DetalharQrcodePost(data)

    return jsonify(response.json()), response.status_code



# Necessário finalizar
@env_pagamento_pix_bp.route('/v2/gn/pix/<id>/qrcode', methods=['PUT'])
def pagar_qrcode_pix(id):
    data = request.get_data()
    if not data:
        return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED})
    else:
        response = utils_envio_pagamento.PagarQrcodePixPut(id, data)

    return jsonify(response.json()), response.status_code