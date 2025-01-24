import string
import random

def CreateE2eid():
    caracteres = string.ascii_letters + string.digits  # Letras e números
    return ''.join(random.choices(caracteres, k=32))


e2eid = CreateE2eid()
print(e2eid)
