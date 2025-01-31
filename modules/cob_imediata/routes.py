from flask import Blueprint, jsonify, request, redirect, url_for, json, render_template
import cob_imediata.utils_cob as utils_cob, settings.error_messages as error_messages, requests
from urllib.parse import quote
import pay_location.utils_plocation as utils_plocation

cob_imediata_bp = Blueprint('cob_imediata', __name__)

## ------------------------------------------- Bloco Rotas Cobrança Imediata Postman--------------------------------------------------------------------------------------- ##

@cob_imediata_bp.route('/v2/cob', methods=['POST'])
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




# Consultar lista de cobranças
@cob_imediata_bp.route('/v2/cob', methods=['GET'])
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
@cob_imediata_bp.route('/v2/cob/<txid>', methods=['GET'])
def cob_imediata_txid_get(txid):
    # Valida se o parâmetro foi passado
    if not txid:
        return jsonify({'error': error_messages.ERROR_PARAMETER_TXID}), 400
    
    lenghtid = len(txid)

    if 26 <= lenghtid <= 35:
        # Código a ser executado se a condição for verdadeira
        response = utils_cob.CobImediataTxidGet(txid)

        # Verifica se a resposta da API foi bem-sucedida
        if response.status_code == 200:
            response_data = response.json()

            # Campos da resposta
            pix_details = {
                "calendario": response_data.get("calendario"),
                "devedor": response_data.get("devedor"),
                "cpf": response_data.get("cpf"),
                "nome": response_data.get("nome"),
                "valor": response_data.get("valor"),
                "chave": response_data.get("chave"),
                "pixCopiaECola": response_data.get("pixCopiaECola"),
                "revisao": response_data.get("revisao"),
                "solicitacaoPagador": response_data.get("solicitacaoPagador"),
                "txid": response_data.get("txid"),
                "status": response_data.get("status"),
            }
            loc_id = response_data.get("loc", {}).get("id")

            # Verifica se o loc_id existe antes de fazer a requisição externa
            if loc_id:
                #external_url = f"https://efi.comnectlupa.com.br:5000/v2/loc/{loc_id}/qrcode"  # URL completa
                #external_response = requests.get(external_url)
                response = utils_plocation.PayLocationTxidQrcodeGet(loc_id)
                if response.status_code == 200:
                    external_data = response.json()

                #if external_response.status_code == 200:
                #    external_data = external_response.json()

                    # Passando a imagem do QR Code também
                    imagem_qrcode = external_data.get("imagemQrcode")  # Supondo que o campo correto seja esse

                    # Passando todos os dados para o frontend
                    return render_template("cob_imediata_get_txid.html", 
                                           pix=pix_details, 
                                           loc_id=loc_id, 
                                           link_visualizacao=external_data.get("linkVisualizacao", "Link não disponível"),
                                           qr_code_image=imagem_qrcode)  # Passando a imagem do QR Code
            else:
                return jsonify({'error': 'Falha ao chamar o endpoint externo', 'details': external_data.json()}), external_data.status_code

        return jsonify({
            'error': error_messages.ERROR_INVALID_REQUEST,
            'details': response.json()
        }), response.status_code

    



# Criar cobrança imediata (com txid)
@cob_imediata_bp.route('/v2/cob/<txid>', methods=['PUT'])
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
@cob_imediata_bp.route('/v2/cob/<id>', methods=['PATCH'])
def cob_imediata_txid_patch(id):
    data = request.get_json()
    lenghtid = len(id)
    # Valida se os parâmetros foram passados
    if not id or not data:
        return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED}), 400
    
    elif 26 <= lenghtid <= 35:
        response = utils_cob.CobImediataTxidPatch(id, data)

    return jsonify(response.json()), response.status_code
        