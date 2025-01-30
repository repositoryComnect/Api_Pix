from flask import Blueprint, jsonify, request, render_template, redirect, flash, url_for
import authenticate.utils as utils
from flask_login import login_user, logout_user, login_required, current_user
from settings.extensions import db, bcrypt, login_manager
from application.models.models import User



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
    

