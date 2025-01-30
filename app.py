import sys
import os
import logging

# Adiciona a pasta "modules" ao caminho de busca do Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from flask import Flask
from authenticate.routes import auth_bp
from modules.cob_imediata.routes import cob_imediata_bp
from modules.cob_vencimento.routes import cob_vencimento_bp
from modules.gestao_pix.routes import gest_pix_bp
from modules.pay_location.routes import pay_location_bp
from modules.cob_lote.routes import cob_lote_bp
from modules.envio_pagamento_pix.routes import env_pagamento_pix_bp
from modules.template_modules.render_pix.routes import routes_pix_bp
from modules.template_modules.render_cob_imediata.routes import cob_imediata_tp
from modules.template_modules.render_cob_imediata.utils import cob_imediata_ut
from authenticate.login.routes import login_bp
from modules.webhook.routes import webhook_bp
from settings.extensions import db, bcrypt, login_manager
from settings.credentials import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from application.models.models import User
from flask_migrate import Migrate
from flask_cors import CORS

# ---------------------------------------------------------------------------------------- Configuração Logs --------------------------------------------------------------------------------------------------------------------#
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Caminho do arquivo de log
log_file = os.path.join(log_directory, "app.log")

# Configuração básica de logging
logging.basicConfig(level=logging.DEBUG,  # Nível mínimo de log (INFO)
                    format='%(asctime)s - %(levelname)s - %(message)s')  # Formato do log

# Criação de um logger
logger = logging.getLogger(__name__)

# Criação do FileHandler para escrever os logs no arquivo
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)  # Defina o nível do arquivo para INFO
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Adiciona o FileHandler ao logger
logger.addHandler(file_handler)

# Criação do StreamHandler para exibir logs no console
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)  # Defina o nível de exibição no console
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Adiciona o StreamHandler ao logger
logger.addHandler(stream_handler)

# Teste de logging
logger.info("Sistema iniciado com sucesso.")

# ---------------------------------------------------------------------------------------- Flask ---------------------------------------------------------------------------------------------------------------------------------#

# Inicialização do app Flask
app = Flask(__name__)

# ---------------------------------------------------------------------------------------- Rotas ---------------------------------------------------------------------------------------------------------------------------------#
# Registro de Blueprints
app.register_blueprint(auth_bp)  # Autenticação
app.register_blueprint(cob_imediata_bp)  # Cobrança imediata
app.register_blueprint(cob_vencimento_bp)  # Cobrança com vencimento
app.register_blueprint(gest_pix_bp)  # Gestão de PIX
app.register_blueprint(pay_location_bp)  # Payload location
app.register_blueprint(cob_lote_bp)  # Cobrança em lote
app.register_blueprint(env_pagamento_pix_bp)  # Envio e pagamento PIX
app.register_blueprint(routes_pix_bp)  # Template para cobranças PIX
app.register_blueprint(cob_imediata_tp)  # Template de cobrança imediata
app.register_blueprint(webhook_bp)  # Webhook
app.register_blueprint(login_bp)  # Login
app.register_blueprint(cob_imediata_ut) # Utilidades cobrança imediata para poder realizar a exportação de dados CSV
#app.register_blueprint(cob_imediata_pg) # Rota para cobrança via plugin

# ---------------------------------------------------------------------------------- Configurações Gerais -----------------------------------------------------------------------------------------------------------------------#
app.config.from_object(Config)

# Criação da interface de administração
admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap3')

# Criar view personalizada para admins
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin.add_view(AdminModelView(User, db.session))

# Inicialização das extensões
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login.login'  # Nome do blueprint + nome da função de login


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

migrate = Migrate(app, db)

# ---------------------------------------------------------------------------------- Teste Extensão ------------------------------------------------------------------------------------------------------------------------#

# Permite CORS para todas as origens
CORS(app)

# Ou para permitir CORS apenas em uma rota específica
CORS(app, resources={r"/v2/cob": {"origins": "chrome-extension://emmnehnlpjjnfmnanaegbjjblpaaoeib"}})

# --------------------------------------------------------------------------------- Configuração de Certificados SSL -------------------------------------------------------------------------------------------------------#
ssl_context = (
    os.path.join(os.path.dirname(__file__), 'authenticate', 'ssl_authentication', 'fullchain.pem'),
    os.path.join(os.path.dirname(__file__), 'authenticate', 'ssl_authentication', 'comnectlupa_wildcard.com.br.key')
)

# --------------------------------------------------------------------------------- Inicialização do Servidor --------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    # Rodando o servidor Flask com suporte a HTTPS
    # Inicialização do banco de dados
    with app.app_context():
        db.create_all()  # Criação das tabelas no banco
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=ssl_context)
