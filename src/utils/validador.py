# src/utils/validador.py
def es_entero(valor):
    try:
        int(valor)
        return True
    except:
        return False

def es_numero(valor):
    try:
        float(valor)
        return True
    except:
        return False
