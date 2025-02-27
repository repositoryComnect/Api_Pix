from flask import Blueprint, jsonify, request, render_template
import modules.cob_vencimento_postman.utils_cobv as utils_cobv
import pay_location_postman.utils_plocation as utils_plocation
from datetime import datetime


cob_vencimento_tp = Blueprint('cob_vencimento_tp', __name__)

@cob_vencimento_tp.route('/cob_vencimento_put', methods=["POST"])
def cob_vencimento_put():
    # Recebendo dados do formulário
    txid = request.form.get('txid')

    # Função auxiliar para garantir que o valor é um inteiro válido
    def get_int_value(value, default=1):
        try:
            # Tenta converter para int, se falhar retorna o valor default
            return int(value)
        except ValueError:
            return default

    # Construção do payload
    payload = {
        "calendario": {
            "dataDeVencimento": request.form.get('dataDeVencimento'),  # Formato de data YYYY-MM-DD
            "validadeAposVencimento": get_int_value(request.form.get('validadeAposVencimento'))
        },
        "devedor": {
            "cnpj": request.form.get('cnpj'),  # Garantindo que é CNPJ
            "nome": request.form.get('nome'),
            "email": request.form.get('email'),
            "logradouro": request.form.get('logradouro'),
            "cidade": request.form.get('cidade'),
            "uf": request.form.get('uf'),
            "cep": request.form.get('cep')
        },
        "valor": {
            "original": request.form.get('valorOriginal'),  # Valor original como string com duas casas decimais
            "abatimento": {
                "modalidade": get_int_value(request.form.get('abatimentoModalidade', '1')),  # Se não houver valor, define 1
                "valorPerc": get_int_value(request.form.get('abatimentoValorPerc', "0.00"))
            },
            "desconto": {
                "modalidade": get_int_value(request.form.get('descontoModalidade', '1')),
                "descontoDataFixa": [{
                    "data": request.form.get('descontoDataFixa'),
                    "valorPerc": get_int_value(request.form.get('descontoValorPerc', "0.00")),
                }]
            },
            "juros": {
                "modalidade": get_int_value(request.form.get('jurosModalidade', '1')),
                "valorPerc": get_int_value(request.form.get('jurosValorPerc', '0.00'))
            },
            "multa": {
                "modalidade": get_int_value(request.form.get('multaModalidade', '1')),
                "valorPerc": get_int_value(request.form.get('multaValorPerc', '1.00')),
            }
        },
        "chave": request.form.get('chave'),
        "solicitacaoPagador": request.form.get('solicitacaoPagador', "None"),
        "infoAdicionais": [
            {
                "nome": request.form.get('infoAdicionaisNome', "Campo 1"),
                "valor": request.form.get('infoAdicionaisValor', "Informação Adicional1 do PSP-Recebedor")
            }
        ]
    }

    # Chamando a função para processar o pagamento
    response = utils_cobv.CobVencimentoTxidPut(txid, payload)
    response_data = response.json()

    # Verificando se houve erro na resposta
    if response.status_code != 200:  # ou outro código de erro relevante
        # Exibe o erro no template
        return render_template("cob_vencimento_put.html", pix=response_data)

    # Caso contrário, exibe os detalhes da cobrança
    return render_template("cob_vencimento_put.html", pix=response_data)




@cob_vencimento_tp.route('/cob_vencimento_patch', methods=["POST"])
def cob_vencimento_patch():
    txid = request.form.get('txid')
    payload = {
        "devedor": {
            "logradouro" : request.form.get('logradouro'),
            "cidade": request.form.get('cidade'),
            "uf": request.form.get('uf'),
            "cep": request.form.get('cep'),
            "cpf": request.form.get('cpf'),
            "nome": request.form.get('nome')
        },
        "valor": {
        "original": request.form.get('valorOriginal')
        },
        "solicitacaoPagador": request.form.get('solicitacaoPagador')

    }
    try:
            # Faz a chamada à função de processamento
        response = utils_cobv.CobVencimentoTxidPatch(txid, payload)


            # Processa a resposta
        if response.status_code == 200:
            response_data = response.json()  # Captura os dados retornados
            return render_template('cob_vencimento_patch.html', pix=response_data)  # Passa os dados para o template
           
    except Exception as e:
            # Lida com erros durante o processamento
        return render_template('cob_vencimento_patch.html', pix=None, error=str(e))


    return jsonify(response.json()), response.status_code




@cob_vencimento_tp.route('/cob_vencimento_get', methods=["GET", "POST"])
def cob_vencimento_get():
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
    response = utils_cobv.CobVencimentoGet(inicio_formatado, fim_formatado)

    if response.status_code == 200:
        cobs = response.json().get('cobs', [])
        period = {
            "inicio": inicio_formatado,
            "fim": fim_formatado
            }
        return render_template('cob_vencimento_get.html', cobs=cobs, period=period)
    else:
        return jsonify({'error': 'Erro ao buscar cobranças', 'details': response.text}), response.status_code


@cob_vencimento_tp.route('/cob_vencimento_get_txid', methods=["GET", "POST"])
def cob_vencimento_get_txid():
    txid = request.form.get('txid')
    if not txid:
        return jsonify({'error': 'TxId não fornecido'}), 400
    
    # Validação do tamanho do txid
    lenghtid = len(txid)
    if 26 <= lenghtid <= 35:
        # Código a ser executado se a condição for verdadeira
        response = utils_cobv.CobVencimentoTxidGet(txid)

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
                "solicitacaoPagador": response_data.get("solicitacaoPagador"),
                "txid": response_data.get("txid"),
                "status": response_data.get("status"),
            }
        
        loc_id = response_data.get("loc", {}).get("id")

        if loc_id:
            response = utils_plocation.PayLocationTxidQrcodeGet(loc_id)
            if response.status_code == 200:
                external_data = response.json()

                imagem_qrcode = external_data.get("imagemQrcode")  # Supondo que o campo correto seja esse

                    # Passando todos os dados para o frontend
                return render_template("cob_vencimento_get_txid.html", 
                                           pix=pix_details, 
                                           loc_id=loc_id, 
                                           link_visualizacao=external_data.get("linkVisualizacao", "Link não disponível"),
                                           qr_code_image=imagem_qrcode)
            else:
                return jsonify({'error': 'Falha ao chamar o endpoint externo', 'details': external_data.json()}), external_data.status_code

        return jsonify({'error': 'Requisição inválida', 'details': response.json()}), response.status_code


    return jsonify(response.json()), response.status_code