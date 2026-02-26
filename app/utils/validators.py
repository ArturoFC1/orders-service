import re

from app.models.type_definitions import ArticuloDict

# Esta clase define validaciones reutilizables


def validar_articulo(item: ArticuloDict) -> bool:
    match item:
        case {"precio": (int() | float()) as price, "cantidad": int(quantity)}:
            return price >= 0 and quantity > 0
        case _:
            return False


def validar_nombre_cliente(nombre: str) -> bool:
    return bool(re.match(r"^[A-Za-z\s]+$", nombre))
