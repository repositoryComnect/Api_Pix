from flask import Blueprint, render_template, request, json, redirect, url_for, jsonify, request
import cob_imediata.utils_cob as utils_cob

# Crie o Blueprint para a documentação
cob_imediata_tp = Blueprint('cob_imediata_tp', __name__)

# Rota para exibir a documentação
@cob_imediata_tp.route('/cob_imediata', methods=['GET', 'POST'])
def documentacao():
    return render_template('cob_imediata.html')



#  Rota e método de request template GET
@cob_imediata_tp.route('/cob_imediata_get', methods=['GET'])
def get_cobrancas():
    cobs = request.args.get('cobs')
    cobs = json.loads(cobs)  # Converte a string de volta para um objeto JSON
    return render_template('cob_imediata_get.html', cobs=cobs)



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



    