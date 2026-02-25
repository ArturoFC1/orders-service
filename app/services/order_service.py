from app.models.order import Order
from app.models.type_definitions import Calculable
from app.utils.validators import validar_nombre_cliente

# Esta clase aplica logica del negocio


class OrderService:
    def __init__(self, pedidos: list[Order]):
        self.pedidos = pedidos

    def calcular_total(self, order: Calculable) -> float:
        total = 0.0
        for articulo in order.articulos:
            if not articulo.es_valido():
                print(f"Articulo invalido en la orden {order.id}")
                continue
            total += articulo.subtotal()
        return total

    def filtrar_pedidos_caros(self, min_total: float) -> list[Order]:
        return [
            order for order in self.pedidos if self.calcular_total(order) >= min_total
        ]

    def validar_clientes(self) -> None:
        for order in self.pedidos:
            if not validar_nombre_cliente(order.cliente):
                print(f"\nNombre del cliente invalido en la orden: {order.id}\n")
