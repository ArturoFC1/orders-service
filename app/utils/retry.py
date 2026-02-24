import time
from functools import wraps

# Esta clase define reinetentos del servidor con Wrapper


def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        intentos = 3

        for intento in range(intentos):
            try:
                return func(*args, **kwargs)

            except Exception as e:
                print(f"Fallo: {e} | intento {intento+1}/{intentos}")
                time.sleep(2)

        raise Exception("La operacion fallo despues de varios intentos")

    return wrapper
