from flask import Blueprint, jsonify, render_template, request
import modules.cob_boleto_postman.utils_boleto as utils_boleto
import settings.error_messages as error_messages, json
import barcode, os, io, base64
from barcode.writer import ImageWriter

cob_boleto_tp = Blueprint('cob_boleto_tp', __name__)


@cob_boleto_tp.route('/cob_boleto_post', methods=['POST'])
def cob_boleto_post():
    # Criar o dicionário de dados para a API
    data_file = {
        "items": [{
            "name": request.form.get('productName'),
            "value": int(request.form.get('value')),
            "amount": int(request.form.get('amount')),
        }],
        "shippings": [{
            "name": "Default Shipping Cost",
            "value": 100  # Exemplo de valor de frete
        }],
        "payment": {
            "banking_billet": {
                "expire_at": request.form.get('expire'),  # Data de expiração
                "customer": {
                    "name": request.form.get('paymentName').strip(),
                    "cpf": request.form.get('paymentCpf'),
                }
            }
        }
    }

    print(data_file)

    try:
        # Chamar a função para enviar os dados
        response = utils_boleto.CobBoletoOneStepPost(data_file)
        print(response.status_code)

        if response.status_code == 200:
            response_data = response.json()
            print(response_data)

            boleto = {
                "data": {
                    "barcode": response_data.get('data', {}).get('barcode'),
                    "link": response_data.get('data', {}).get('link'),
                    "billet_link": response_data.get('data', {}).get('billet_link'),
                    "pdf": response_data.get('data', {}).get('pdf', {}).get('charge'),
                    "expire_at": response_data.get('data', {}).get('expire_at'),
                    "charge_id": response_data.get('data', {}).get('charge_id'),
                    "status": response_data.get('data', {}).get('status'),
                    "total": response_data.get('data', {}).get('total')
                }
            }

            barcode_number = response_data.get('data', {}).get('barcode')
            barcode_image = None

            if barcode_number:
                barcode_format = barcode.get_barcode_class("code128")
                if barcode_format:
                    barcode_instance = barcode_format(barcode_number, writer=ImageWriter())

                    buffer = io.BytesIO()
                    barcode_instance.write(buffer)
                    barcode_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

            return render_template('cob_boleto_post.html', boleto=boleto, barcode_image=barcode_image)
        else:
            return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    