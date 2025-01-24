from flask import Blueprint, jsonify, request
import cob_vencimento.utils_cobv as utils_cobv, random, authenticate.utils as utils, settings.error_messages as error_messages

cob_vencimento_bp = Blueprint('cob_vencimento', __name__)


## ------------------------------------------- Bloco Rotas Cobrança Com Vencimento ------------------------------------------------------------------------ ##
# Rota de cobrança com vencimento GET - essa rota exije que seja fornecido como parâmetro a data de inicio e fim, ex(?inicio=2020-10-22T16:01:35Z&fim=2020-11-30T20:10:00Z)




@cob_vencimento_bp.route('/v2/cobv', methods=['GET'])
def cob_vencimento_get():

    # Obtém os parâmetros da URL
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')

    # Valida se os parâmetros foram passados
    if not inicio or not fim:
        return jsonify({'error': error_messages.ERROR_MISSING_PARAMETERS}), 400
    else:
        response = utils_cobv.CobVencimentoGet(inicio, fim)

    return jsonify(response.json()), response.status_code
    





@cob_vencimento_bp.route('/v2/cobv/<id>', methods=['GET'])
def cob_vencimento_txid_get(id):
    lenghtid = len(id)

    # Valida se os parâmetros foram passados
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_TXID}), 400
    
    elif 26 <= lenghtid <= 35:
        response = utils_cobv.CobVencimentoTxidGet(id)
    
    else:
        return jsonify({'error': error_messages.ERROR_LENGTH_PARAMETER}), 400

    return jsonify(response.json()), response.status_code
    




@cob_vencimento_bp.route('/v2/cobv/<id>', methods=['PUT'])
def cob_vencimento_txid_put(id):
    data = request.get_json()  # Obtém o JSON enviado no corpo da requisição

    # Verifica se os campos obrigatórios estão presentes
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_TXID}), 400

    if not data:
        return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED}), 400

    calendario = data.get('calendario')
    devedor = data.get('devedor')
    valor = data.get('valor')
    chave = data.get('chave')

    # Valida se os campos obrigatórios estão no JSON
    if not calendario or not devedor or not valor or not chave:
        return jsonify({'error': error_messages.ERROR_FIELD_MANDATORY}), 400

    # Processa a lógica principal
    response = utils_cobv.CobVencimentoTxidPut(id, data)

    # Retorna a resposta
    return jsonify(response.json()), response.status_code
    



    

@cob_vencimento_bp.route('/v2/cobv/<id>', methods=['PATCH'])
def cob_vencimento_txid_patch(id):
    data = request.get_json()
    lenghtid = len(id)
    if not id:
        return jsonify({'error': error_messages.ERROR_PARAMETER_TXID}), 400
    
    if not data:
        return jsonify({'error': error_messages.ERROR_PAYLOAD_NOT_PROVIDED}), 400
    
    if 26 <= lenghtid <= 35:
        response = utils_cobv.CobVencimentoTxidPatch(id, data)

    else:
       return jsonify({'error': error_messages.ERROR_LENGTH_PARAMETER}), 400 

    return jsonify(response.json()), response.status_code