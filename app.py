import logging, requests, os, sys
from waitress import serve
#from app import app  # ou o nome do seu aplicativo Flask
import ssl

# Adiciona a pasta "modules" ao caminho de busca do Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from flask import Flask
from authenticate.routes import auth_bp

# Imports Postman
from modules.cob_imediata_postman.routes import cob_imediata_pt
from modules.cob_vencimento_postman.routes import cob_vencimento_pt
from modules.gestao_pix_postman.routes import gest_pix_pt
from modules.pay_location_postman.routes import pay_location_pt
from modules.cob_lote_postman.routes import cob_lote_pt
from modules.envio_pagamento_pix_postman.routes import env_pagamento_pix_pt
from modules.cob_boleto_postman.routes import cob_boleto_pt

# Imports render template
from modules.template_modules.render_cob_imediata.routes import cob_imediata_tp
from modules.template_modules.render_cob_vencimento.routes import cob_vencimento_tp
from modules.template_modules.render_webhook.routes import web_tp

# Import de utilidades
from modules.template_modules.render_cob_imediata.utils import cob_imediata_ut

# Import extensão chrome
from modules.cob_imediata_plugin.routes import cob_imediata_pg
from flask_cors import CORS

# Import login 
from authenticate.login.routes import login_bp
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from application.models.models import User

# Import Webhooks 
from modules.webhook.routes import webhook_wh

# Imports DB
from flask_pymongo import PyMongo
from settings.extensions import db, bcrypt, login_manager, mongo
from settings.credentials import Config
from flask_migrate import Migrate




# ---------------------------------------------------------------------------------------- Configuração Logs --------------------------------------------------------------------------------------------------------------------#
# Criar diretório de logs se não existir
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Caminho do arquivo de log
log_file = os.path.join(log_directory, "app.log")

# Configuração básica de logging
logging.basicConfig(
    level=logging.DEBUG,  # Captura todos os logs a partir do nível DEBUG
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),  # Salva os logs no arquivo
        logging.StreamHandler(sys.stdout)  # Exibe logs no terminal
    ],
)

# Criar um logger específico para a aplicação
logger = logging.getLogger(__name__)

# Habilitar logs detalhados de requisições HTTP (requests e urllib3)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.DEBUG)

# Para capturar todas as requisições HTTP no Flask
logging.getLogger("werkzeug").setLevel(logging.DEBUG)
# Reduzir o nível de log do pymongo
logging.getLogger("pymongo").setLevel(logging.WARNING)



# ---------------------------------------------------------------------------------------- Flask ---------------------------------------------------------------------------------------------------------------------------------#

# Inicialização do app Flask
app = Flask(__name__, template_folder='templates')

# ---------------------------------------------------------------------------------------- Rotas ---------------------------------------------------------------------------------------------------------------------------------#
# Registro de Blueprints

# Blueprint rota de autenticação
app.register_blueprint(auth_bp)  # Autenticação

# Blueprint rotas Postman
app.register_blueprint(cob_imediata_pt)  # Cobrança imediata Postman
app.register_blueprint(cob_vencimento_pt)  # Cobrança com vencimento 
app.register_blueprint(gest_pix_pt)  # Gestão de PIX
app.register_blueprint(pay_location_pt)  # Payload location
app.register_blueprint(cob_lote_pt)  # Cobrança em lote
app.register_blueprint(env_pagamento_pix_pt)  # Envio e pagamento PIX
app.register_blueprint(cob_boleto_pt) # Cobranças com boleto

# Blueprint rotas de templates
app.register_blueprint(cob_imediata_tp)  # Template de cobrança imediata
app.register_blueprint(cob_vencimento_tp) # Rota cobrança vencimento
app.register_blueprint(web_tp)

# Blueprint rota configuração de Webhook
app.register_blueprint(webhook_wh)  # Webhook

# Blueprint rota de Login
app.register_blueprint(login_bp)  # Login

# Blueprint rota de utilidade
app.register_blueprint(cob_imediata_ut) # Utilidades cobrança imediata para poder realizar a exportação de dados 

# Blueprint rota extensão Google Chrome
app.register_blueprint(cob_imediata_pg) # Rota cobrança imediata plugin chrome


# ---------------------------------------------------------------------------------- Configurações Gerais -----------------------------------------------------------------------------------------------------------------------#
app.config.from_object(Config)

# Criação da interface de administração
admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap3')

# Criar view personalizada para admins
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin.add_view(AdminModelView(User, db.session))

# Inicializa as extensões
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mongo.init_app(app)  # Inicialize o PyMongo com o app

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

# Caminhos para os arquivos de certificado e chave
'''cert_file = os.path.join(os.path.dirname(__file__), 'authenticate', 'ssl_authentication', '_.comnect.com.br', 'fullchainEfi.pem')
key_file = os.path.join(os.path.dirname(__file__), 'authenticate', 'ssl_authentication', '_.comnect.com.br', 'comnect_wildcard_2024.key')
chain_file = os.path.join(os.path.dirname(__file__), 'authenticate', 'authentication_webhook', 'certificate-chain-homolog.crt')

# Criação do contexto SSL com suporte explícito ao TLS 1.2 e 1.3
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)

# Adicionando a cadeia de certificados intermediários
ssl_context.load_verify_locations(cafile=chain_file)'''

def run_server(port):
    # Executando o servidor Flask com SSL
    app.run(host='0.0.0.0', port=port ) #'ssl_context=ssl_context'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Criação das tabelas no banco
    serve(app, host='0.0.0.0', port=5000,  threads=10)
