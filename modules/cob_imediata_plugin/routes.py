from flask import Blueprint, jsonify, request
import cob_imediata_postman.utils_cob as utils_cob, settings.error_messages as error_messages, requests
import pay_location_postman.utils_plocation as utils_plocation

cob_imediata_pg = Blueprint('cob_imediata_pg', __name__)

@cob_imediata_pg.route('/cob_imediata_plugin', methods=['POST'])
def cob_imediata_plugin():
    if request.is_json:
        data = request.get_json()
        if not data:
            return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED}), 400

        calendario = data.get('calendario')
        valor = data.get('valor')
        chave = data.get('chave')

        if not calendario or not valor or not chave:
            return jsonify({'error': error_messages.ERROR_FIELD_MANDATORY}), 400

    try:
        response = utils_cob.CobImediataPost(data)

        if isinstance(response, tuple):
            return response

        if response.status_code == 201:
            response_data = response.json()

            loc_id = response_data.get("loc", {}).get("id")  # Pegando ID dentro de "loc"
            pix_copia_e_cola = response_data.get("pixCopiaECola")  # Código do Pix

            # Chamar o outro endpoint para buscar o QR Code e link de visualização
            response = utils_plocation.PayLocationTxidQrcodeGet(loc_id)
            if response.status_code == 200:
                external_data = response.json()

                return jsonify({
                    "qrcodeImagem": external_data.get("imagemQrcode"),
                    "pixCopiaECola": pix_copia_e_cola,
                    "linkVisualizacao": external_data.get("linkVisualizacao", "Link não disponível")
                }), 200
            else:
                return jsonify({'error': 'Falha ao chamar o endpoint externo', 'details': external_data.json()}), external_data.status_code

        return jsonify({
            'error': error_messages.ERROR_INVALID_REQUEST,
            'details': response.json()
        }), response.status_code

    except Exception as e:
        return jsonify({'error': error_messages.ERROR_INVALID_REQUEST + str(e)}), 500
