from flask import Blueprint, render_template, send_file, request, jsonify
import qrcode
from io import BytesIO
import json
from urllib.parse import unquote

routes_pix_bp = Blueprint('routes', __name__)

@routes_pix_bp.route('/gerar_pix')
def gerar_pix():
    # Receber os dados como string JSON codificada na URL
    pix_details_json = request.args.get('pix_details')

    if not pix_details_json:
        return jsonify({'error': 'Dados insuficientes para renderizar o QR Code'}), 400

    try:
        # Decodificar JSON da URL
        pix_details = json.loads(unquote(pix_details_json))

        # Gerar QR Code
        pix_copia_e_cola = pix_details.get("pixCopiaECola")
        if not pix_copia_e_cola:
            return jsonify({'error': 'Copia e cola do Pix está ausente nos dados'}), 400
        
        # Criar QR Code como imagem PIL
        qr = qrcode.make(pix_copia_e_cola)

        # Salvar QR Code em memória
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        # Renderizar o template com os dados
        return render_template("pix.html", pix=pix_details, qr_code_url="/qr_code_image?pix_details=" + unquote(pix_details_json))
    except Exception as e:
        print(f"Erro ao processar pix_details: {e}")
        return jsonify({'error': f'Erro ao processar pix_details: {e}'}), 500


@routes_pix_bp.route('/qr_code_image')
def qr_code_image():
    # Receber os dados do QR Code como string JSON codificada na URL
    pix_details_json = request.args.get('pix_details')

    if not pix_details_json:
        return jsonify({'error': 'Dados insuficientes para gerar o QR Code'}), 400

    try:
        # Decodificar JSON da URL
        pix_details = json.loads(unquote(pix_details_json))
        pix_copia_e_cola = pix_details.get("pixCopiaECola")
        if not pix_copia_e_cola:
            return jsonify({'error': 'Copia e cola do Pix está ausente nos dados'}), 400

        # Gerar QR Code
        qr = qrcode.make(pix_copia_e_cola)

        # Salvar QR Code em memória
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        # Retornar a imagem gerada como resposta
        return send_file(buffer, mimetype="image/png")
    except Exception as e:
        print(f"Erro ao gerar QR Code: {e}")
        return jsonify({'error': f'Erro ao gerar QR Code: {e}'}), 500



@routes_pix_bp.route('/qr_code_image_txid')
def qr_code_image_txid():
    pix_details_json = request.args.get('pix_details')
    if not pix_details_json:
        return jsonify({'error': 'Dados insuficientes para renderizar o QR Code'}), 400
    try:
        # Decodificar JSON da URL
        pix_details = json.loads(unquote(pix_details_json))

        # Gerar QR Code
        pix_copia_e_cola = pix_details.get("pixCopiaECola")
        if not pix_copia_e_cola:
            return jsonify({'error': 'Copia e cola do Pix está ausente nos dados'}), 400
        
        # Criar QR Code como imagem PIL
        qr = qrcode.make(pix_copia_e_cola)

        # Salvar QR Code em memória
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        # Renderizar o template com os dados
        return render_template("cob_imediata_get_txid.html", pix=pix_details, qr_code_url="/qr_code_image?pix_details=" + unquote(pix_details_json))
    except Exception as e:
        print(f"Erro ao processar pix_details: {e}")
        return jsonify({'error': f'Erro ao processar pix_details: {e}'}), 500
