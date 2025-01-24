import string
import random

def CreateTxid(lengh=26):
    caracteres = string.ascii_letters + string.digits  # Letras e números
    txid = ''.join(random.choices(caracteres, k=lengh))  # Gera um Txid de 16 caracteres
    print("Txid gerado:", txid)

txid = CreateTxid()

print(txid)
