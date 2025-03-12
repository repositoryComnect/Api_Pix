from flask import jsonify


# Mensagens de erros genéricas

ERROR_MISSING_PARAMETERS = 'Parâmetros "inicio" e "fim" são obrigatórios'
ERROR_PAYLOAD_NOT_PROVIDED = 'Payload não foi fornecido'
ERROR_INVALID_REQUEST = 'Erro ao processar a solicitação'
ERROR_CONNECTION_ABORTED = 'Erro de conexão: A conexão foi abortada'
ERROR_PARAMETER_ID = 'Parâmetro "ID" não foi fornecido'
ERROR_PARAMETER_TXID = 'Parâmetro "TXID" não foi fornecido'
ERROR_FIELD_MANDATORY = 'Campos obrigatórios não foram fornecidos'
ERROR_LENGTH_PARAMETER = 'O parâmetro está com seu formato errado'
ERROR_PARAMETER_E2EID = 'Parâmetro "E2EID" não foi fornecido'
ERROR_PARAMETERS = 'Os parâmetros necessários não foram fornecidos'
ERROR_NUMERIC_ID = 'O parâmetro "ID" deve ser numérico'
ERROR_JSON_INVALIDO = 'A resposta da API externa não contém um JSON válido.'
ERROR_FORMATED_PAYLOAD = 'O payload não está com o formato de acordo'
ERROR_BILLET_NOT_CREATED = 'Erro no processo de geração do boleto'



def MessageCampoObrigatorio():

    return jsonify({'error': ERROR_FIELD_MANDATORY}), 400


def MessagePayloadNaoFornecido():

    return jsonify({'error': ERROR_PAYLOAD_NOT_PROVIDED}), 400


def MessageParametrosInicioFim():
        
    return jsonify({'error': ERROR_MISSING_PARAMETERS}), 400


def MessageIdNaoFornecido():

    return jsonify({'error': ERROR_PARAMETER_ID}), 400


def MessageTxidNaoFornecido():

    return jsonify({'error': ERROR_PARAMETER_TXID}), 400