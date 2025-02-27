# Rota base PIX

URL_BASE_PIX_H = "https://pix-h.api.efipay.com.br"
URL_BASE_PIX_P = "https://pix.api.efipay.com.br"

# URL da API de autenticação
AUTH_URL_H = URL_BASE_PIX_H + "/oauth/token"  # Para ambiente de Desenvolvimento Homologação 
AUTH_URL_P = URL_BASE_PIX_P + "/oauth/token" # Para ambiente de Desenvolvimento Produção

# URL da API de cobrança imediata
URL_COBIMEDIATA_H = URL_BASE_PIX_H + "/v2/cob"
URL_COBIMEDIATA_P = URL_BASE_PIX_P + "/v2/cob"

# URL da API de cobranças com vencimento
URL_COBVENCIMENTO_H = URL_BASE_PIX_H + "/v2/cobv"
URL_COBVENCIMENTO_P = URL_BASE_PIX_P + "/v2/cobv"

# URL da API de gestão de pix
URL_GESTPIX_H = URL_BASE_PIX_H + "/v2/pix"
URL_GESTPIX_P = URL_BASE_PIX_P + "/v2/pix"

# URL da API de Payloads Location
URL_PAYLOCATIONS_H = URL_BASE_PIX_H + "/v2/loc"
URL_PAYLOCATIONS_P = URL_BASE_PIX_P + "/v2/loc"

# URL da API para cobranças em lote
URL_COBLOTE_H = URL_BASE_PIX_H + "/v2/lotecobv"
URL_COBLOTE_P = URL_BASE_PIX_P + "/v2/lotecobv"

URL_REQUISITAR_ENVIO_PIX_H = URL_BASE_PIX_H + "/v3/gn/pix"
URL_REQUISITAR_ENVIO_PIX_P = URL_BASE_PIX_P + "/v3/gn/pix"

URL_ENVIO_PAGAMENTO_PIX_H = URL_BASE_PIX_H + "/v2/gn"
URL_ENVIO_PAGAMENTO_PIX_P = URL_BASE_PIX_P + "/v2/gn"

# URL da para o Webhook 
URL_WEBHOOK_H = URL_BASE_PIX_H + "/v2/webhook"
URL_WEBHOOK_P = URL_BASE_PIX_P + "/v2/webhook"


# Rota base API Cobranças (Boleto, Cartão, Carnê, Link de pagamento)
URL_BASE_COB_H = "https://cobrancas-h.api.efipay.com.br"
URL_BASE_COB_P = "https://cobrancas.api.efipay.com.br"

# Rota de autenticação
AUTH_URL_COB_H = URL_BASE_COB_H + "/v1/authorize"
AUTH_URL_COB_P = URL_BASE_COB_P + "/v1/authorize"

# Rota de criação de boleto ONE-STEP
URL_BOLETO_ONE_STEP_H = URL_BASE_COB_H + "/v1/charge/one-step"
URL_BOLETO_ONE_STEP_P = URL_BASE_COB_P + "/v1/charge/one-step"


URL_BOLETO_H = URL_BASE_COB_H + "/v1/charge"
URL_BOLETO_P = URL_BASE_COB_P + "/v1/charge"