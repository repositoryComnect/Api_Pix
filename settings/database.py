from settings.extensions import db
from flask import current_app

def init_db(app):
    with app.app_context():
        # Certifique-se de que estamos no contexto correto
        if current_app is None:
            raise RuntimeError("O contexto da aplicação Flask não está ativo!")
        db.create_all()  # Apenas cria as tabelas