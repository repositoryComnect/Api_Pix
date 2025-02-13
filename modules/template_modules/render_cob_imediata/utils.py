import csv
from io import StringIO
from flask import Blueprint, request, make_response, jsonify
from modules.cob_imediata_postman.utils_cob import CobImediataGet
from datetime import datetime

cob_imediata_ut = Blueprint('cob_imediata_ut', __name__)


# Rota para poder gerar uma exportação CSV
@cob_imediata_ut.route('/exportar', methods=['GET'])
def exportar():
    # Recupera as datas
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')

    # Verificar se as datas não estão vazias
    if not inicio or not fim:
        return jsonify({'error': 'Datas não fornecidas ou estão vazias'}), 400

    try:
        # Tenta converter para o formato completo com hora
        inicio_formatado = datetime.strptime(inicio, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ')
        fim_formatado = datetime.strptime(fim, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        try:
            # Se não funcionar, tenta o formato só com a data
            inicio_formatado = datetime.strptime(inicio, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
            fim_formatado = datetime.strptime(fim, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            return jsonify({'error': 'Formato de data inválido'}), 400

    try:
        # Chama a função que busca as cobranças
        response = CobImediataGet(inicio_formatado, fim_formatado)
        if response.status_code == 200:
            cobs = response.json().get('cobs', [])
        else:
            return jsonify({'error': 'Erro ao buscar cobranças', 'details': response.text}), response.status_code
    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor', 'details': str(e)}), 500

    # Criação do CSV em memória
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Data de Criação', 'Expiração', 'Chave', 'CPF do Devedor', 'Nome do Devedor', 'Revisão', 'Solicitação do Pagador', 'Status', 'TXID', 'Valor'])

    # Preencher as linhas do CSV com as cobranças
    for cob in cobs:
        writer.writerow([cob.get('calendario', {}).get('criacao', ''),
                         cob.get('calendario', {}).get('expiracao', ''),
                         cob.get('chave', ''),
                         cob.get('devedor', {}).get('cpf', ''),
                         cob.get('devedor', {}).get('nome', ''),
                         cob.get('revisao', ''),
                         cob.get('solicitacaoPagador', ''),
                         cob.get('status', ''),
                         cob.get('txid', ''),
                         cob.get('valor', {}).get('original', '')])

    # Cria a resposta com o arquivo CSV
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=cobrancas.csv"
    response.headers["Content-Type"] = "text/csv"
    return response