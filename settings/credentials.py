import os


# Credenciais de acesso
credentials = {
    "client_id": "Client_Id_e8d44b81f25e9aa1cf3dc67afc62f5e684314dce",
    "client_secret": "Client_Secret_965850baff064bd55435ce2950857fa9faf0f556",
    "certificate" : r'C:\Users\WNB\OneDrive - Wireless Networks do Brasil LTDA\Área de Trabalho\API Pix\authenticate\certificado.pem'
}

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuração do MongoDB
    MONGO_URI = "mongodb://localhost:27017/webhook"

    SECRET_KEY = os.urandom(24)  # Defina uma chave secreta segura
