from flask import Blueprint, jsonify
import authenticate.utils as utils


auth_bp = Blueprint('authenticate', __name__)

## ------------------------------------------- Bloco Rotas authenticate -------------------------------------------------------------------------------------------- ##

# Obter Autorização
@auth_bp.route('/oauth/token', methods=['POST'])
def get_token():
    token = utils.authenticate()
    if token:
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"error": "Failed to fetch token"}), 500
    

@auth_bp.route('/v1/authorize', methods=['POST'])
def get_token_cob():
    token = utils.authenticateCobranca()
    if token:
        return jsonify({"access_token": token}), 200
    
    else:
        return jsonify({"error": "Erro ao tentar obter o token"}), 500
    

