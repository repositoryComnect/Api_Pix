import sys
import os
import base64

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
from modules.webhook.routes import webhook_bp

app = Flask(__name__)

# App Pix
app.register_blueprint(auth_bp) # Inicializa a rota de autenticação
app.register_blueprint(cob_imediata_bp) # Inicializa as rotas de cobrança imediata
app.register_blueprint(cob_vencimento_bp) # Inicializa as rotas de cobrança com vencimento
app.register_blueprint(gest_pix_bp) # Inicializa as rotas de gestão de pix
app.register_blueprint(pay_location_bp) # Inicializa as rotas de payload location
app.register_blueprint(cob_lote_bp) # Inicializa as rotas de cobrança lote
app.register_blueprint(env_pagamento_pix_bp) # Inicializa as rotas de envio e pagamento pix


# Rotas Templates
app.register_blueprint(routes_pix_bp)# Rota que renderiza a cobrança de pix
app.register_blueprint(cob_imediata_tp)# Rota que renderiza a cobrança de pix

# Rota Webhook
app.register_blueprint(webhook_bp)



# Registrar o filtro personalizado
@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

app.secret_key = os.urandom(24)  # Defina uma chave secreta para a sessão

# Certificados SSL
ssl_context = (
    os.path.join(os.path.dirname(__file__), 'authenticate', 'ssl_authentication', 'cert.pem'),  # Caminho para o certificado
    os.path.join(os.path.dirname(__file__), 'authenticate', 'ssl_authentication', 'key.pem')   # Caminho para a chave privada
)

if __name__ == '__main__':
    # Rodando o servidor Flask com suporte a HTTPS
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=ssl_context)
   