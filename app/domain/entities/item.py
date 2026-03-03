from dataclasses import dataclass

# Esta clase valida y calcula subtotal


@dataclass
class Item:
    nombre: str
    precio: float
    cantidad: int

    def es_valido(self) -> bool:
        return self.precio >= 0 and self.cantidad > 0

    def subtotal(self) -> float:
        return self.precio * self.cantidad
