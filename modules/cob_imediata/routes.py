from flask import Blueprint, jsonify, request, redirect, url_for, json, session
import cob_imediata.utils_cob as utils_cob, settings.error_messages as error_messages
from urllib.parse import quote
import re
from datetime import datetime


cob_imediata_bp = Blueprint('cob_imediata', __name__)

## ------------------------------------------- Bloco Rotas Cobrança Imediata --------------------------------------------------------------------------------------- ##

# Criar cobrança imediata (sem txid)
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
    else:
        try:
            # Validando e processando o payload do formulário
            valor_original = request.form.get("valor[original]", "")
            if not valor_original:
                raise ValueError("Campo 'valor[original]' é obrigatório.")

            # Validando o formato do valor (regex)
            if not re.match(r"^[0-9]{1,10}\.[0-9]{2}$", valor_original):
                raise ValueError(
                    "Campo 'valor[original]' deve estar no formato '0.00' com até 10 dígitos antes do ponto."
                )
            data = {
                "calendario": {
                    "expiracao": int(request.form.get("calendario[expiracao]", 3600))
                },
                "devedor": {
                    "cpf": request.form.get("devedor[cpf]", ""),
                    "nome": request.form.get("devedor[nome]", "")
                },
                "valor": {
                    "original": valor_original
                },
                "chave": request.form.get("chave", ""),
                "solicitacaoPagador": request.form.get("solicitacaoPagador", "")
            }
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

    try:
        response = utils_cob.CobImediataPost(data)

        if isinstance(response, tuple):
            return response

        if response.status_code == 201:
            response_data = response.json()

            # Campos da resposta
            pix_details = {
                "calendario": response_data.get("calendario"),
                "devedor": response_data.get("devedor"),
                "valor": response_data.get("valor"),
                "chave": response_data.get("chave"),
                "pixCopiaECola": response_data.get("pixCopiaECola"),
                "status": response_data.get("status"),
            }

            print(pix_details)

            # Codificar pix_details em JSON e então codificar para URL
            encoded_pix_details = quote(json.dumps(pix_details))

            # Redirecionar para gerar o Pix
            return redirect(url_for('routes.gerar_pix', pix_details=encoded_pix_details))
            #return jsonify(response.json()), response.status_code Linha para depuração

        return jsonify({
            'error': error_messages.ERROR_INVALID_REQUEST,
            'details': response.json()
        }), response.status_code

    except Exception as e:
        return jsonify({'error': error_messages.ERROR_INVALID_REQUEST + str(e)}), 500




    
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
        try:
            # Tenta converter as datas no formato 'YYYY-MM-DD'
            inicio_formatado = datetime.strptime(inicio, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
            fim_formatado = datetime.strptime(fim, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            try:
                # Se falhar, tenta converter as datas no formato 'YYYY-MM-DDTHH:MM:SSZ'
                inicio_formatado = datetime.strptime(inicio, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ')
                fim_formatado = datetime.strptime(fim, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                return jsonify({'error': 'Formato de data inválido'}), 400

        response = utils_cob.CobImediataGet(inicio_formatado, fim_formatado)

    # Redireciona para a rota get_cobrancas com os dados como parâmetros de consulta
    return redirect(url_for('cob_imediata_tp.get_cobrancas', cobs=json.dumps(response.json()['cobs'])))




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

    #Validar a partir daqui
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

            # Codificar pix_details em JSON e então codificar para URL
            encoded_pix_details = quote(json.dumps(pix_details))

            # Redirecionar para gerar o Pix
            return redirect(url_for('routes.qr_code_image_txid', pix_details=encoded_pix_details)) 
    else:
        return jsonify({'error': error_messages.ERROR_LENGTH_PARAMETER}), 400 

    #return jsonify(response.json()), response.status_code
    



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
        return jsonify({'error': 'O payload não está com o formato de acordo'})



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
        