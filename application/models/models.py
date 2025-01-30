from settings.extensions import db
from flask_login import UserMixin  # Importe UserMixin

class User(db.Model, UserMixin):  # Adicione UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Tamanho adequado para senha criptografada
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"

    # Métodos obrigatórios do Flask-Login
    def is_active(self):
        # Retorna True se o usuário estiver ativo (você pode modificar a lógica conforme necessário)
        return True  # Aqui, estamos considerando que todos os usuários são ativos

    def get_id(self):
        return str(self.id)  # Retorna o ID do usuário como string (necessário para Flask-Login)

    def is_authenticated(self):
        # Retorna True se o usuário estiver autenticado
        return True

    def is_anonymous(self):
        # Retorna True se o usuário for anônimo (não autenticado)
        return False
