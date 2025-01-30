from flask import Blueprint, render_template, request, redirect, url_for, jsonify, request, json
from flask_login import login_required
import cob_imediata.utils_cob as utils_cob
from datetime import datetime
import settings.error_messages as error_messages
from urllib.parse import quote
import re
from urllib.parse import unquote

# Crie o Blueprint para a documentação
cob_imediata_tp = Blueprint('cob_imediata_tp', __name__)

# Rota para exibir a documentação
@cob_imediata_tp.route('/', methods=['GET', 'POST'])
@login_required
def documentacao():
    return render_template('cob_imediata.html')



@cob_imediata_tp.route('/cob_imediata_post', methods=['POST'])
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
                "loc_id": response_data.get("loc", {}).get("id")  # Pegando ID dentro de "loc"
            }
            loc_id = response_data.get("loc", {}).get("id")  # Pegando ID dentro de "loc"


            # Codificar pix_details em JSON e então codificar para URL
            pix_details_json = quote(json.dumps(pix_details))

            # Redirecionar para gerar o Pix
            return render_template("pix.html", pix=pix_details, loc_id=loc_id, qr_code_url="/qr_code_image?pix_details=" + unquote(pix_details_json))
            #return redirect(url_for('routes.gerar_pix', pix_details=encoded_pix_details))
            #return jsonify(response.json()), response.status_code 

        return jsonify({
            'error': error_messages.ERROR_INVALID_REQUEST,
            'details': response.json()
        }), response.status_code

    except Exception as e:
        return jsonify({'error': error_messages.ERROR_INVALID_REQUEST + str(e)}), 500




@cob_imediata_tp.route('/cob_imediata_get', methods=['POST'])
def get_cobrancas():
    inicio = request.form.get('inicio')
    fim = request.form.get('fim')

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

    # Chama a função utilitária para buscar as cobranças
    try:
        response = utils_cob.CobImediataGet(inicio_formatado, fim_formatado)
        if response.status_code == 200:
            cobs = response.json().get('cobs', [])
            period = {
                "inicio": inicio_formatado,
                "fim": fim_formatado
            }
            return render_template('cob_imediata_get.html', cobs=cobs, period=period)
        else:
            return jsonify({'error': 'Erro ao buscar cobranças', 'details': response.text}), response.status_code
    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor', 'details': str(e)}), 500
    



#  Rota e método de request template GET TXID
@cob_imediata_tp.route('/process_txid', methods=['POST'])
def process_txid():
    txid = request.form.get('txid')
    return redirect(url_for('cob_imediata.cob_imediata_txid_get', txid = txid))



# Rota e método de request template PUT 
@cob_imediata_tp.route('/process_txid_put', methods=['POST'])
def process_txid_put():
    # Obtém os dados do formulário
    txid = request.form.get('txid')
    if not txid:
        return jsonify({"error": "TxId não foi fornecido"}), 400

    data = {
        "calendario": {
            "expiracao": int(request.form.get("calendario[expiracao]", 3600))
        },
        "devedor": {
            "cpf": request.form.get("devedor[cpf]", ""),
            "nome": request.form.get("devedor[nome]", "")
        },
        "valor": {
            "original": request.form.get("valor[original]", "")
        },
        "chave": request.form.get("chave", ""),
        "solicitacaoPagador": request.form.get("solicitacaoPagador", "")
    }


    # Faz a chamada à função de processamento
    response = utils_cob.CobImediataTxidPut(txid, data)
    response_data = response.json()

    if response.status_code == 201:
    # Renderiza o template com os dados da cobrança
        return render_template("cob_imediata_put_txid.html", pix=response_data)

    else:
        return render_template("cob_imediata_put_txid.html", pix=response_data)
    



# Rota e método de request template PATCH 
@cob_imediata_tp.route('/process_patch', methods=['POST'])
def process_patch():
    # Verifica o método simulado
    if request.form.get('_method') == 'PATCH':
        txid = request.form.get('txid')

        # Estrutura do payload conforme esperado pela API
        data = {
            "calendario": {
                "expiracao": int(request.form.get("calendario[expiracao]", 600))  # Tempo padrão de expiração
            },
            "devedor": {
                "nome": request.form.get("devedor[nome]", ""),
                "cpf": request.form.get("devedor[cpf]", "")
            },
            "valor": {
                "original": request.form.get("valor[original]", "0.00")  # Valor padrão
            },
            "chave": request.form.get("chave", ""),  # Campo 'chave' adicionado
            "solicitacaoPagador": request.form.get("solicitacaoPagador", ""),
            "infoAdicionais": [
                {
                    "nome": "Nome 1",
                    "valor": request.form.get("infoAdicionais[valor]", "valor 1")
                }
            ]
        }

        try:
            # Faz a chamada à função de processamento
            response = utils_cob.CobImediataTxidPatch(txid, data)

            # Processa a resposta
            if response.status_code == 200:
                response_data = response.json()  # Captura os dados retornados
                print(response_data)
                return render_template('cob_imediata_patch_txid.html', pix=response_data)  # Passa os dados para o template
           
        except Exception as e:
            # Lida com erros durante o processamento
            return render_template('cob_imediata_patch_txid.html', pix=None, error=str(e))



    