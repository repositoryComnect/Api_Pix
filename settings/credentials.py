import os


# Credenciais de acesso
credentials = {
    "client_id": "Client_Id_486b1e4e17223413adaecbee4821da036bc61ca6",
    "client_secret": "Client_Secret_b0ab68a12bf197ebc505e25c25b48b38ecaffa78",
    "certificate" : r'C:\Users\WNB\OneDrive - Wireless Networks do Brasil LTDA\Área de Trabalho\API Pix\authenticate\homologacao-670788-APIEfi_cert.pem'
}

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Defina uma chave secreta segura
